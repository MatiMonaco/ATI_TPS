import numpy as np
from filters.filter import Filter
from PyQt5 import QtWidgets,QtCore

from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter


class Canny(Filter):

    def __init__(self, update_callback): 
        super().__init__()
        self.update_callback = update_callback
        self.sobel_filter = SobelFilter(update_callback)
        self.prewitt_filter = PrewittFilter(update_callback)
        self.current_filter  = self.sobel_filter
        self.t1 = 0
        self.t2 = 100
        self.setupUI()

    def setupUI(self):
       
        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)
 

        self.gradient_filter_label = QtWidgets.QLabel(self.groupBox)
        self.gradient_filter_label.setText("<html><head/><body><span><p>&Delta;I algorithm</></span></body></html>")
        self.gradient_filter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gradient_filter_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.gradient_filter_label)

        self.cb = QtWidgets.QComboBox()
        self.cb.addItems(["Sobel", "Prewitt"])
        self.cb.currentIndexChanged.connect(self.selectionchange) 
        self.horizontalLayout.addWidget(self.cb)

        line = QtWidgets.QFrame(self.groupBox)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line)

        self.t1_label = QtWidgets.QLabel(self.groupBox)
        self.t1_label.setText("t1")
        self.t1_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.t1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.t1_label)

        self.t1_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.t1_line_edit.setStyleSheet("font-weight:bold;")
        self.horizontalLayout.addWidget(self.t1_line_edit)


        self.t2_label = QtWidgets.QLabel(self.groupBox)
        self.t2_label.setText("t2")
        self.t2_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.t2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.t2_label)
        self.t2_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.t2_line_edit.setStyleSheet("font-weight:bold;")
        self.horizontalLayout.addWidget(self.t2_line_edit)

        line2 = QtWidgets.QFrame(self.groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line2)
        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
      
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)


        # self.horizontalLayout.setStretch(0, 1)
        # self.horizontalLayout.setStretch(1, 1)
        # self.horizontalLayout.setStretch(2, 1)
        # self.horizontalLayout.setStretch(3, 1)
        # self.horizontalLayout.setStretch(4, 1)
        # self.horizontalLayout.setStretch(5, 1)
        # self.horizontalLayout.setStretch(6, 1)

    def selectionchange(self,i):
        if i == 0:
            self.current_filter = self.sobel_filter
        else:
            self.current_filter = self.prewitt_filter
        

    def apply(self, img):

        # 1. Suavizamiento y diferenciación --> es pasarle la mask de Gauss pero NO hay que hacerlo!! 
        # 2. Obtener la dirección perpendicular al borde (aplicar sobel o prewitt)
        edge_magnitude_image =  self.current_filter.apply(img) # TODO parametrizar para que sea sobel o prewitt y que retornen tmb dx y dy (ahora solo retornan la sintesis y encima ya normalizada, creo que hay que manejarla sin normalizar todavia aca)
        dx_image,dy_image = self.current_filter.get_gradient()

        # 3. Ángulo del gradiente para estimar la direccion ortogonal al borde

        direction_angle = self.discretize_angle(np.arctan(dy_image/ dx_image)*180/np.pi) # Si dy = 0 arctan2 lo convierte en +-90º

        # 4. Supresión de no máximos
        self.no_max_supression(edge_magnitude_image, direction_angle)

        # 5. Umbralización con histéresis
        
                 


    def discretize_angle(self,angle): 
        print("prev angle = ",angle)
        if angle < 0:
            angle+=180
            print("new angle = ",angle)
        if (angle >= 0 and angle <= 22.5) or (angle >= 157.5 and angle <= 180): 
            discretized_angle = 0
        
        elif angle > 22.5 and angle <= 67.5:
            discretized_angle = 45 
        
        elif angle > 67.5 and angle <= 112.5:
            discretized_angle = 90
        
        else: 
            discretized_angle = 135 

        return discretized_angle

    def no_max_supression(self, edge_magnitude_image, direction): 

        for row in edge_magnitude_image.shape[0]: # TODO ojo con cual es el height y el width que la pifeo siempre
            for col in edge_magnitude_image.shape[1]:

                curr_pixel = edge_magnitude_image[row, col] # Para cada pixel con magnitud de borde no cero, inspeccionar los pixels adyacentes indicados en la dirección ortogonal al su borde.
                if curr_pixel != 0:                     
                    adjacent_pixels = self.get_adjacent_pixels(curr_pixel, direction)

                    # Si la magnitud de cualquiera de los dos pixels adyacentes es mayor que la del pixel en cuestión, entonces borrarlo como borde.
        
    def get_adjacent_pixels(self, curr_pixel, direction):
        pass


