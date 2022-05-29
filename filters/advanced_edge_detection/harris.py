from dis import dis
import numpy as np
import matplotlib.pyplot as plt

from filters.filter import Filter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator
from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter 
from filters.spatial_domain.gauss_mask import GaussMaskFilter 
from PIL import Image, ImageDraw
import math 

class Harris(Filter):


    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback

        self.sobel_filter = SobelFilter(update_callback)
        self.prewitt_filter = PrewittFilter(update_callback)
        self.gauss_filter = GaussMaskFilter(update_callback)
        self.current_filter = self.sobel_filter

        self.max_edges_amount = 3000
        self.gauss_filter.sigma = 3
      
        self.threshold = 1000
    
        self.setupUI()
 

    def setupUI(self):
        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)
        # self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        # self.verticalLayout.addLayout(self.horizontalLayout2)
        onlyInt = QIntValidator()
        onlyInt.setBottom(0)
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

        self.sigma_label = QtWidgets.QLabel(self.groupBox)
        self.sigma_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.sigma_label.setScaledContents(False)
        self.sigma_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sigma_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&sigma;</></span></pre></body></html>")
        self.horizontalLayout.addWidget(self.sigma_label)

        self.sigma_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.sigma_line_edit.setValidator(onlyInt)
        self.sigma_line_edit.editingFinished.connect(
            lambda: self.gauss_filter.setSigma(self.sigma_line_edit.text()))
        self.sigma_line_edit.setText(str(self.gauss_filter.sigma))
        self.horizontalLayout.addWidget(self.sigma_line_edit)

        line3 = QtWidgets.QFrame(self.groupBox)
        line3.setFrameShape(QtWidgets.QFrame.VLine)
        line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line3)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)
        

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
        dx2,dy2, dxy = self.apply_gauss_mask()

        # 3. Calcular valor de respuesta de Harris
        response = self.calculate_response(dx2, dy2, dxy)

        # 4. Buscar los maximos 
        print("response: ",response)
        top_n_indexes = self.get_n_max_values(response)
        print(f"Max indexes ({top_n_indexes.shape}) = ",top_n_indexes)
        print("response > 0 :",response[top_n_indexes[:,0],top_n_indexes[:,1]])

        # 5. Retorno imagen con los edges pintados.
        if self.isGrayScale:
            img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1]))
            img_arr = np.repeat(img_arr[:, :, np.newaxis], 3, axis=2)

        img = Image.fromarray(img_arr.astype(np.uint8), 'RGB')
        draw = ImageDraw.Draw(img)
        radius = 2
        for y,x,z in top_n_indexes:

            draw.ellipse((x-radius,  y-radius, x +radius,  y+radius), fill="red", outline='red')   
        #img_arr[top_n_indexes[:,0],top_n_indexes[:,1]] = np.array([255,0,0])

        # for idx in top_n_indexes:
        #     x = idx[0]
        #     y = idx[1]
          
        return  np.asarray(img)

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
        #print("RESPONSE")
        #print(response)
        
        return np.argwhere(response > self.threshold)
 
        #return max_edges_list[:self.max_edges_percentage * len(max_edges_list)]
        # Response es una matriz de numeros, los pixeles que tengan mayor response se corresponden con las esquinas (entiendo que se corresponden por indice)    
        n = self.max_edges_amount
        print(n)
        idx = np.argpartition(response, response.size-n, axis=None)[-1:-(n+1):-1]  # Devuelve los n indices mas grandes de mas grande a mas chico como si fuese un array 1D
        
        return np.array(list(zip(*np.unravel_index(idx, response.shape)))) # Convierto los indices 1D en indices de un array con shape arr.shape

    def get_n_max_values(self, response): 
        n = self.max_edges_amount
        print(n)
        idx = np.argpartition(response, response.size-n, axis=None)[-1:-(n+1):-1]  # Devuelve los n indices mas grandes de mas grande a mas chico como si fuese un array 1D
        
        return np.array(list(zip(*np.unravel_index(idx, response.shape)))) # Convierto los indices 1D en indices de un array con shape arr.shape
