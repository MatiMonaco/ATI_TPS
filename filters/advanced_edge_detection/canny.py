from dis import dis
import numpy as np
import matplotlib.pyplot as plt
from filters.filter import Filter
from PyQt5 import QtWidgets,QtCore

from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter
from PyQt5.QtGui import QDoubleValidator

class Canny(Filter):

    def __init__(self, update_callback): 
        super().__init__()
        self.update_callback = update_callback
        self.sobel_filter = SobelFilter(update_callback)

        self.prewitt_filter = PrewittFilter(update_callback)
        self.current_filter  = self.sobel_filter
        self.t1 = 0
        self.t2 = 100
        self.directions = self.conection_directions(False)
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

        onlyDouble = QDoubleValidator()
        onlyDouble.setBottom(0)
        

        self.t1_label = QtWidgets.QLabel(self.groupBox)
        self.t1_label.setText("t1")
        self.t1_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.t1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.t1_label)

        self.t1_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.t1_line_edit.setStyleSheet("font-weight:bold;")
        self.t1_line_edit.setValidator(onlyDouble)
        self.horizontalLayout.addWidget(self.t1_line_edit)


        self.t2_label = QtWidgets.QLabel(self.groupBox)
        self.t2_label.setText("t2")
        self.t2_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.t2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.t2_label)
        self.t2_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.t2_line_edit.setStyleSheet("font-weight:bold;")
        self.t2_line_edit.setValidator(onlyDouble)
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

        self.t1_line_edit.textChanged.connect(self.setT1)
        self.t2_line_edit.textChanged.connect(self.setT2)
        # self.horizontalLayout.setStretch(0, 1)
        # self.horizontalLayout.setStretch(1, 1)
        # self.horizontalLayout.setStretch(2, 1)
        # self.horizontalLayout.setStretch(3, 1)
        # self.horizontalLayout.setStretch(4, 1)
        # self.horizontalLayout.setStretch(5, 1)
        # self.horizontalLayout.setStretch(6, 1)

    def setT1(self,text):
        if text != '':
            self.t1 = float(text)
            print("T1 changed to ",self.t1)

    def setT2(self,text):
        if text != '':
            self.t2 = float(text)
            print("T2 changed to ",self.t2)

    def selectionchange(self,i):
        if i == 0:
            self.current_filter = self.sobel_filter
        else:
            self.current_filter = self.prewitt_filter
        

    def apply(self, img_arr):
        self.current_filter.channels = self.channels
        print("canny channels = ",self.channels)
        # 1. Suavizamiento y diferenciación --> es pasarle la mask de Gauss pero NO hay que hacerlo!! 
        # 2. Obtener la dirección perpendicular al borde (aplicar sobel o prewitt)
        edge_magnitude_image =  self.current_filter.apply(img_arr) 
        dx_image,dy_image = self.current_filter.get_gradient()
        print(f"dx = {dx_image.shape}")
        print(f"edge_magnitude_image = {edge_magnitude_image.shape}")

        edge_magnitude_image_aux =  edge_magnitude_image.copy()

        # 3. Ángulo del gradiente para estimar la direccion ortogonal al borde
        angles  = np.arctan2(dy_image, dx_image)*180/np.pi
        print("angles = ",angles)
      
        # 4. Supresión de no máximos
        image = self.no_max_supression(edge_magnitude_image, angles)
        no_max_image = image.copy() 

        # 5. Umbralización con histéresis
        image = self.hysteresis_threshold(image)
        thresholding_image = image.copy() 

        self.plot_intermediate_images(edge_magnitude_image_aux, no_max_image, thresholding_image)

        return image
        
    def conection_directions(self, check_4: bool = True):
        return [
            [-1, 0], #top
            [0, -1], #left
            [0, 1], #right
            [1, 0] #bottom
            ] if check_4 else [
            [-1, 0], #top
            [0, -1], #left
            [0, 1], #right
            [1, 0], #bottom
            [-1, -1], #top-left
            [-1, 1], #top-right
            [1, -1], #bottom-left
            [1, 1] #bottom-right
            ]
            
    def has_border_connection(self, img: np.ndarray, h_pos: int, w_pos: int, channel: int) -> bool:
        width  = img.shape[1]
        height = img.shape[0]
        neighbor_idxs = np.array([h_pos, w_pos]) + self.directions
        for n_coord in list(neighbor_idxs):
            if self.in_bounds(n_coord[0], n_coord[1], width, height) and img[n_coord[0], n_coord[1], channel] == 255: # si mi vecino está dentro de la img y mi vecino es borde --> soy borde
                return True
        return False

        
    def hysteresis_threshold(self, img: np.ndarray) -> np.ndarray:
        width  = img.shape[1]
        height = img.shape[0]
        
        print(img[:,:,:self.channels] > self.t2)
        img[img[:,:,:self.channels] > self.t2] = 255
        print(img[:,:,:self.channels] > self.t2)

        # print(img[:,:,:self.channels] < self.t1)
        img[img[:,:,:self.channels] < self.t1] = 0
        # print(img[img[:,:,:self.channels] < self.t1])

        # entre t1 y t2 busco conectitud 
        for i in range(height): 
            for j in range(width):
                for channel in range(0,self.channels):
                    if img[i,j,channel] <= self.t2 and img[i,j,channel] >= self.t1 and self.has_border_connection(img, i, j, channel):
                        img[i,j,channel] = 255
        
        for j in range(width): 
            for i in range(height):
                for channel in range(0,self.channels):
                    if img[i,j,channel] <= self.t2 and img[i,j,channel] >= self.t1 and self.has_border_connection(img, i, j, channel):
                        img[i,j,channel] = 255

        
        # Si < t1 o estas entre t1 y t2 pero no tenes vecinos bordes
        img[img[:,:,:self.channels] != 255] = 0
        print(img[img[:,:,:self.channels] != 255])
        return img

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
        for i in range(height): 
            for j in range(width):
            
                for channel in range(0,self.channels):
                       
                    curr_pixel_magnitude = edge_magnitude_image[i, j,channel] # Para cada pixel con magnitud de borde no cero, inspeccionar los pixels adyacentes indicados en la dirección ortogonal al su borde.
                    if curr_pixel_magnitude != 0:
                        # Agarro los 2 pixeles adyacentes en la direción del gradiente
                        dirX ,dirY  = self.discretize_angle(angles[i,j,channel])
                        adj_px1_i,adj_px1_j =  i+dirX,j+dirY
                        adj_px2_i,adj_px2_j =  i-dirX,j-dirY

                        # Chequear que esten dentro de la imagen, sino= 0       
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
              
    def plot_intermediate_images(self,edge_magnitude_image, no_max_image, thresholding_image ): 

        plt.ion()
        fig,(ax1, ax2, ax3) = plt.subplots(1,3, sharey=True)

        edge_magnitude_image = self.correct_if_gray(edge_magnitude_image)
        no_max_image = self.correct_if_gray(no_max_image)
        thresholding_image= self.correct_if_gray(thresholding_image)

        ax1.imshow(edge_magnitude_image.astype('int32'))
        ax1.set_title("Edge Detector Synthesis")
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax2.imshow(no_max_image.astype('int32'))
        ax2.set_title("No Max Supression")
        ax2.set_yticklabels([])
        ax2.set_xticklabels([])
        ax3.imshow(thresholding_image.astype('int32'))
        ax3.set_title("Thresholding")
        ax3.set_yticklabels([])
        ax3.set_xticklabels([])
        plt.show()
    
    def correct_if_gray(self, gray_array):
        if gray_array.shape[2] == 1:
           res = np.empty((gray_array.shape[0], gray_array.shape[1], 3))
           res[:, :, 0:3] = gray_array
           return res

        return gray_array



    def name(self):
            return "Canny Filter"

