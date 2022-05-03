from dis import dis
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
        self.current_filter.channels = self.channels
        print("canny channels = ",self.channels)
        # 1. Suavizamiento y diferenciación --> es pasarle la mask de Gauss pero NO hay que hacerlo!! 
        # 2. Obtener la dirección perpendicular al borde (aplicar sobel o prewitt)
        edge_magnitude_image =  self.current_filter.apply(img) 
        dx_image,dy_image = self.current_filter.get_gradient()
        print(f"dx = {dx_image.shape}")
        print(f"edge_magnitude_image = {edge_magnitude_image.shape}")


        # 3. Ángulo del gradiente para estimar la direccion ortogonal al borde
        angles  = np.arctan2(dy_image, dx_image)*180/np.pi
        print("angles = ",angles.shape)
      
        # 3. Supresión de no máximos
        edge_magnitude_image = self.no_max_supression(edge_magnitude_image, angles)

        # 4. Umbralización con histéresis
        return edge_magnitude_image
        
                 


    def discretize_angle(self,angle): 
       
        if angle < 0:
            angle+=180
        
        if (angle >= 0 and angle <= 22.5) or (angle >= 157.5 and angle <= 180): 
            dirX,dirY = 1,0 # 0
        
        elif angle > 22.5 and angle <= 67.5:
            dirX,dirY = 1,-1 # 45
        
        elif angle > 67.5 and angle <= 112.5:
            dirX,dirY = 0,-1 # 90
        
        else: 
            dirX,dirY = -1,-1  # 135

        return dirX,dirY


    def in_bounds(self,x,y,w,h):
        return x >= 0 and x < w and y >= 0 and y < h

    def no_max_supression(self, edge_magnitude_image, angles): 
        width  =edge_magnitude_image.shape[1]
        height = edge_magnitude_image.shape[0]
        for i in range(height): # TODO ojo con cual es el height y el width que la pifeo siempre <- esactamente
            for j in range(width):
            
                for channel in range(0,self.channels):
                       
                    curr_pixel_magnitude = edge_magnitude_image[i, j,channel] # Para cada pixel con magnitud de borde no cero, inspeccionar los pixels adyacentes indicados en la dirección ortogonal al su borde.
                    if curr_pixel_magnitude != 0:
                        # Agarro los 2 pixeles adyacentes en la direción del gradiente
                        dirX ,dirY  = self.discretize_angle(angles[i,j,channel])
                        adj_px1_i,adj_px1_j =  i+dirX,j+dirY
                        adj_px2_i,adj_px2_j =  i-dirX,j-dirY       
                        if self.in_bounds(adj_px1_i,adj_px1_j,width,height):
                            adj_px1_magnitude = edge_magnitude_image[adj_px1_i,adj_px1_j,channel]
                        else: 
                            adj_px1_magnitude = 0

                        if self.in_bounds(adj_px2_i,adj_px2_j,width,height):
                            adj_px2_magnitude = edge_magnitude_image[adj_px2_i,adj_px2_j,channel]
                        else: 
                            adj_px2_magnitude = 0
                  
                        # Si la magnitud de cualquiera de los dos pixels adyacentes es mayor que la del pixel en cuestión, entonces borrarlo como borde.
                        if  curr_pixel_magnitude < adj_px1_magnitude or curr_pixel_magnitude < adj_px2_magnitude:
                            edge_magnitude_image[i,j,channel] = 0
               
        return edge_magnitude_image
            
    def name(self):
            return "Canny Filter"

