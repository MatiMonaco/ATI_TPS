from filters.filter import Filter
from libs.TP0.img_operations import normalize

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QDoubleValidator
from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter 
from filters.spatial_domain.gauss_mask import GaussMaskFilter 
from PIL import Image, ImageDraw

import numpy as np

class Harris(Filter):


    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback

        self.sobel_filter = SobelFilter(update_callback)
        self.prewitt_filter = PrewittFilter(update_callback)
        self.gauss_filter = GaussMaskFilter(update_callback)
        self.current_filter = self.sobel_filter

        self.gauss_filter.sigma = 3
      
        self.threshold = 0.2
    
        self.setupUI()

    def algorithmChange(self, i):
        if i == 0:
            self.current_filter = self.sobel_filter
            print("Changed to Sobel filter")
        else:
            self.current_filter = self.prewitt_filter
            print("Changed to Prewitt filter")
                   

    def apply(self, img_arr):
        print(f"apply arr shape: {img_arr.shape}")
        self.current_filter.channels = self.channels
        self.gauss_filter.channels = self.channels

        # 1. Se calculan las derivadas de Prewitt o Sobel      
        self.edge_magnitude_image = self.current_filter.apply(img_arr)
        print("edge magnitude shape = ",self.edge_magnitude_image.shape)
        self.dx_image, self.dy_image = self.current_filter.get_gradient() # la de 0 verticales tiene que ser Ix
      
        # 2. Suavizar con Gauss
        dx2, dy2, dxy = self.apply_gauss_mask()

        # 3. Calcular valor de respuesta de Harris
        response = self.calculate_response(dx2, dy2, dxy)

        # 4. Buscar los maximos 
        print("response: ",response)
        #TODO: normalize response para que sea mas facil setear el treshold
        positives = self.get_positive_values(response)
        # 5. Retorno imagen con los edges pintados.
        if self.isGrayScale:
            img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1]))
            img_arr = np.repeat(img_arr[:, :, np.newaxis], 3, axis=2)

        img     = Image.fromarray(img_arr.astype(np.uint8), 'RGB')
        draw    = ImageDraw.Draw(img)
        radius  = 2
        for y, x, z in positives:
            # print(f"img_arr[{y},{x},{z}] = {img_arr[y, x, z]}, response[{y},{x},{z}] = {response[y, x, z]}")
            draw.ellipse((x-radius,  y-radius, x + radius, y+radius), fill="red", outline='red')
          
        return np.asarray(img)

    def apply_gauss_mask(self): 

        dx2 = self.dx_image**2 #np.linalg.matrix_power(self.dx_image, 2)   chequear que esto sea elemento a elemento
        dy2 = self.dy_image**2 #np.linalg.matrix_power(self.dy_image, 2)

        # Aplico Gauss 7x7 sigma=2 
        dx2_gauss = self.gauss_filter.apply(dx2) # TODO que retorne y que se le puedan setear la mask y sigma
        print("dx2 shape = ",dx2_gauss.shape)
        dy2_gauss = self.gauss_filter.apply(dy2)
        print("dy2_gauss shape = ",dy2_gauss.shape)

        dxy_gauss = self.gauss_filter.apply(self.dx_image * self.dy_image) #  Ix*Iy punto a punto, sin suavizar
        print("dxy_gauss shape = ",dxy_gauss.shape)

        return dx2_gauss, dy2_gauss, dxy_gauss
        
    def calculate_response(self, dx2, dy2, dxy): 
        k = 0.04
        return (dx2*dy2 - dxy**2) - k * (dx2+dy2)**2 # TODO matricial 

    def get_positive_values(self, response):
        negatives_mask = response < 0 # mascara de positivos
        response = np.abs(response)
        response = normalize(response)

        #TODO: ver si queremos ver los bordes no hay que hacer esto jeje
        response[negatives_mask] = 0 # seteamos en 0 los valores negativos

        # Buscar los mayores a treshold, unicamente donde la response era positiva previo a la normalizacion
        return np.argwhere(response > self.threshold)

    ##################################################################################################

    def setTreshold(self, t: tuple):
        # (d, ok) = locale.toDouble("1234,56")
        if t[1]:
            self.threshold = float(t[0])
                

    def name(self):
        return "Harris Corner Detection"

    def setupUI(self):
        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.gradient_filter_label = QtWidgets.QLabel(self.groupBox)
        self.gradient_filter_label.setText(
            "<html><head/><body><span><p>&Delta;I algorithm</></span></body></html>")
        self.gradient_filter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gradient_filter_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.gradient_filter_label)

        self.alg_cb = QtWidgets.QComboBox()
        self.alg_cb.addItems(["Sobel", "Prewitt"])
        self.alg_cb.currentIndexChanged.connect(self.algorithmChange)
        self.horizontalLayout.addWidget(self.alg_cb)

        line = QtWidgets.QFrame(self.groupBox)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line)

        self.threshold_label = QtWidgets.QLabel(self.groupBox)
        self.threshold_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.threshold_label.setScaledContents(False)
        self.threshold_label.setAlignment(QtCore.Qt.AlignCenter)
        self.threshold_label.setText(
            "<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:14px; color:#ffffff; background-color:transparent;\"><p>Threshold</></span></pre></body></html>")
        self.horizontalLayout.addWidget(self.threshold_label)

        double_validator = QDoubleValidator(bottom=0, top=1, decimals=3)
        double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        double_validator.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.threshold_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.threshold_line_edit.setValidator(double_validator)
        self.threshold_line_edit.editingFinished.connect(
            lambda: self.setTreshold(double_validator.locale().toDouble(self.threshold_line_edit.text())))
        self.threshold_line_edit.setText(str(self.threshold))
        self.horizontalLayout.addWidget(self.threshold_line_edit)

        line3 = QtWidgets.QFrame(self.groupBox)
        line3.setFrameShape(QtWidgets.QFrame.VLine)
        line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line3)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)
