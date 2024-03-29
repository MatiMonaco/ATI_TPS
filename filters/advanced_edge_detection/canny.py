from dis import dis
import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.filters import threshold_multiotsu

from filters.filter import Filter
from PyQt5 import QtWidgets, QtCore

from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter
from PyQt5.QtGui import QDoubleValidator


class Canny(Filter):

    def __init__(self, update_callback,setupUI = True):
        super().__init__()
        self.update_callback = update_callback
        self.sobel_filter = SobelFilter(update_callback)

        self.prewitt_filter = PrewittFilter(update_callback)
        self.current_filter = self.sobel_filter
        self.t1 = np.array([110,100,100])
        self.t2 = np.array([220,220,220])
        self.directions = None
        self.connection = 4
        self.use_otsu = False
        self.edge_magnitude_image = None
        self.no_max_image = None
        self.thresholding_image = None
        if setupUI:
            self.setupUI()

    def setupUI(self):

        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout2)

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

        self.conection_cb = QtWidgets.QComboBox()
        self.conection_cb.addItems(["4-connected", "8-connected"])
        self.conection_cb.currentIndexChanged.connect(self.connectionChange)
        self.horizontalLayout.addWidget(self.conection_cb)

        line2 = QtWidgets.QFrame(self.groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line2)


        self.otsu_label = QtWidgets.QLabel(self.groupBox)
        self.otsu_label.setText("Use Otsu")
        self.otsu_label.setStyleSheet("font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.otsu_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.otsu_label)

        self.otsu_check = QtWidgets.QCheckBox()
        self.otsu_check.stateChanged.connect(lambda: self.otsu_state_changed())
        self.horizontalLayout.addWidget(self.otsu_check)

        line3 = QtWidgets.QFrame(self.groupBox)
        line3.setFrameShape(QtWidgets.QFrame.VLine)
        line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line3)

    
        
        self.btn_show_steps = QtWidgets.QPushButton(self.groupBox)
        self.btn_show_steps.clicked.connect(lambda: self.plot_intermediate_images(self.edge_magnitude_image, self.no_max_image, self.thresholding_image))
        self.btn_show_steps.setStyleSheet("font-weight: bold;color:white;")
        self.btn_show_steps.setText("Show steps")
        self.horizontalLayout.addWidget(self.btn_show_steps)


        line4 = QtWidgets.QFrame(self.groupBox)
        line4.setFrameShape(QtWidgets.QFrame.VLine)
        line4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line4)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)


     

        onlyDouble = QDoubleValidator()
        onlyDouble.setBottom(0)

        self.t1_label = QtWidgets.QLabel(self.groupBox)
        self.t1_label.setText("t1")
        self.t1_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.t1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.t1_label)

        self.t1_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.t1_line_edit.setStyleSheet("font-weight:bold;")
        self.t1_line_edit.setValidator(onlyDouble)
        self.horizontalLayout2.addWidget(self.t1_line_edit)

        self.t2_label = QtWidgets.QLabel(self.groupBox)
        self.t2_label.setText("t2")
        self.t2_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.t2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.t2_label)

        self.t2_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.t2_line_edit.setStyleSheet("font-weight:bold;")
        self.t2_line_edit.setValidator(onlyDouble)
        self.horizontalLayout2.addWidget(self.t2_line_edit)



        self.t1_line_edit.textChanged.connect(self.setT1)
        self.t2_line_edit.textChanged.connect(self.setT2)
        self.t1_line_edit.setText(str(self.t1[0]))
        self.t2_line_edit.setText(str(self.t2[0]))


    def setT1(self, text):
        if text != '':
            self.t1[:] = int(text)

    def setT2(self, text):
        if text != '':
            self.t2[:] = int(text)

    def algorithmChange(self, i):
        if i == 0:
            self.current_filter = self.sobel_filter
            print("Changed to Sobel filter")
        else:
            self.current_filter = self.prewitt_filter
            print("Changed to Prewitt filter")

    def connectionChange(self, i):
        if i == 0:
            self.connection = 4
            print("Changed to 4-connected")
        else:
            self.connection = 8
            print("Changed to 8-connected")

    def apply(self, img_arr):
        self.directions = self.conection_directions(self.connection == 4)
        self.current_filter.channels = self.channels
        print("canny channels = ", self.channels)
        # 1. Suavizamiento y diferenciación --> es pasarle la mask de Gauss pero NO hay que hacerlo!!
        # 2. Obtener la dirección perpendicular al borde (aplicar sobel o prewitt)
        edge_magnitude_image = self.current_filter.apply(img_arr)
        dx_image, dy_image = self.current_filter.get_gradient()
     
      

        self.edge_magnitude_image = edge_magnitude_image.copy()

        # 3. Ángulo del gradiente para estimar la direccion ortogonal al borde
        angles = np.arctan2(dx_image, dy_image)#np.pi/2 # pi/2 para agarrar el ortogonal al borde
        angles[angles < 0] += np.pi
        angles = np.pi - angles # 45 to 135, 135 to 45
        #angles[angles > 2*np.pi] -= np.pi
        angles = np.rad2deg(angles)#*180/np.pi
        
         

        if self.use_otsu:
            self.apply_otsu_multilevel(edge_magnitude_image)
 
     
        # 4. Supresión de no máximos
        image = self.no_max_supression(edge_magnitude_image, angles)
        self.no_max_image = image.copy()

        # 5. Umbralización con histéresis
        image = self.hysteresis_threshold(image)
        self.thresholding_image = image.copy()

        # Delete white contour 
        if self.isGrayScale:
            image[0,:] = 0
            image[:,0] = 0
            image[image.shape[0]-1,:] = 0
            image[:,image.shape[1]-1] = 0
        else: 
            image[0,:] = np.array([0,0,0])
            image[:,0] = np.array([0,0,0])
            image[image.shape[0]-1,:] = np.array([0,0,0])
            image[:,image.shape[1]-1] = np.array([0,0,0])



      
        return image

    

    def conection_directions(self, check_4: bool = True):
        return [
            [-1, 0],  # top
            [0, -1],  # left
            [0, 1],  # right
            [1, 0]  # bottom
        ] if check_4 else [
            [-1, 0],  # top
            [0, -1],  # left
            [0, 1],  # right
            [1, 0],  # bottom
            [-1, -1],  # top-left
            [-1, 1],  # top-right
            [1, -1],  # bottom-left
            [1, 1]  # bottom-right
        ]

    def has_border_connection(self, img: np.ndarray, h_pos: int, w_pos: int, channel: int) -> bool:
        width = img.shape[1]
        height = img.shape[0]
        neighbor_idxs = np.array([h_pos, w_pos]) + self.directions
        for n_coord in list(neighbor_idxs):
            # si mi vecino está dentro de la img y mi vecino es borde --> soy borde
            if self.in_bounds(n_coord[1], n_coord[0], width, height) and img[n_coord[0], n_coord[1], channel] == 255:
                return True
        return False

    def hysteresis_threshold(self, img: np.ndarray) -> np.ndarray:
        width = img.shape[1]
        height = img.shape[0]

    
        img[img[:, :, :self.channels] > self.t2[:self.channels]] = 255
        img[img[:, :,:self.channels] < self.t1[:self.channels]] = 0 

        # entre t1 y t2 busco conectitud
        for i in range(height):
            for j in range(width):
                for channel in range(0, self.channels):
                    if img[i, j, channel] <= self.t2[channel] and img[i, j, channel] >= self.t1[channel] and self.has_border_connection(img, i, j, channel):
                        img[i, j, channel] = 255

        for j in range(width):
            for i in range(height):
                for channel in range(0, self.channels):
                    if img[i, j, channel] <= self.t2[channel] and img[i, j, channel] >= self.t1[channel] and self.has_border_connection(img, i, j, channel):
                        img[i, j, channel] = 255

        # Si < t1 o estas entre t1 y t2 pero no tenes vecinos bordes
        img[img[:, :, :self.channels] != 255] = 0
        print(img[img[:, :, :self.channels] != 255])
        return img

    def discretize_angle(self, angle):

        #if angle < 0:
        #    angle += 180

        if (angle >= 0 and angle <= 22.5) or (angle >= 157.5 and angle <= 180):
            dirX, dirY = 1, 0  # 0

        elif angle > 22.5 and angle <= 67.5:
            dirX, dirY = 1, -1  # 45

        elif angle > 67.5 and angle <= 112.5:
            dirX, dirY = 0, -1  # 90

        else:
            dirX, dirY = -1, -1  # 135

        return dirX, dirY

    def in_bounds(self, x, y, w, h):
        return x >= 0 and x < w and y >= 0 and y < h

    def no_max_supression(self, edge_magnitude_image, angles):
        width = edge_magnitude_image.shape[1]
        height = edge_magnitude_image.shape[0]
        for i in range(height):
            for j in range(width):

                for channel in range(0, self.channels):

                    # Para cada pixel con magnitud de borde no cero, inspeccionar los pixels adyacentes indicados en la dirección ortogonal al su borde.
                    curr_pixel_magnitude = edge_magnitude_image[i, j, channel]
                    if curr_pixel_magnitude != 0:
                        # Agarro los 2 pixeles adyacentes en la direción del gradiente
                        dirX, dirY = self.discretize_angle(angles[i, j, channel])

                        adj_px1_i, adj_px1_j = i+dirY, j+dirX
                        adj_px2_i, adj_px2_j = i-dirY, j-dirX

                        # Chequear que esten dentro de la imagen, sino= 0
                        if self.in_bounds(adj_px1_j, adj_px1_i, width, height):
                            adj_px1_magnitude = edge_magnitude_image[adj_px1_i, adj_px1_j, channel]
                        else:
                            adj_px1_magnitude = 0

                        if self.in_bounds(adj_px2_j, adj_px2_i, width, height):
                            adj_px2_magnitude = edge_magnitude_image[adj_px2_i, adj_px2_j, channel]
                        else:
                            adj_px2_magnitude = 0

                        # Si la magnitud de cualquiera de los dos pixels adyacentes es mayor que la del pixel en cuestión, entonces borrarlo como borde.
                        if curr_pixel_magnitude < adj_px1_magnitude or curr_pixel_magnitude < adj_px2_magnitude:
                            edge_magnitude_image[i, j, channel] = 0

        return edge_magnitude_image


    def otsu_state_changed(self):
        self.use_otsu = self.otsu_check.isChecked()
        print("Use Otsu = ",self.use_otsu)

    def apply_otsu_multilevel(self, edge_magnitude_image):
        thresholds = []
        for channel in range(0, self.channels):
            thresholds.append(threshold_multiotsu(edge_magnitude_image[:,:,channel]))
      
        self.t1[:] = int(thresholds[0][0])
        self.t2[:] = int(thresholds[0][1])
        self.t1_line_edit.setText(str(self.t1[0]))
        self.t2_line_edit.setText(str(self.t2[0]))
     
        print(f"t1 rgb {self.t1}")
        print(f"t2 rgb {self.t2}")

    def plot_intermediate_images(self, edge_magnitude_image, no_max_image, thresholding_image):
        if edge_magnitude_image is None or no_max_image is None or thresholding_image is None:
            print("Please apply Canny first!")
            return
        plt.ion()
        fig, axs = plt.subplots(1, 3, sharey=True)

        edge_magnitude_image = self.correct_if_gray(edge_magnitude_image)
        no_max_image = self.correct_if_gray(no_max_image)
        thresholding_image = self.correct_if_gray(thresholding_image)

        # First Row Images
        axs[0].imshow(edge_magnitude_image.astype('int32'))
        axs[0].set_title("Edge Detector Synthesis")
        axs[0].set_yticklabels([])
        axs[0].set_xticklabels([])

        axs[1].imshow(no_max_image.astype('int32'))
        axs[1].set_title("No Max Supression")
        axs[1].set_yticklabels([])
        axs[1].set_xticklabels([])

        axs[2].imshow(thresholding_image.astype('int32'))
        axs[2].set_title("Thresholding")
        axs[2].set_yticklabels([])
        axs[2].set_xticklabels([])


        plt.show()

    def correct_if_gray(self, gray_array):
        if gray_array.shape[2] == 1:
            res = np.empty((gray_array.shape[0], gray_array.shape[1], 3))
            res[:, :, 0:3] = gray_array
            return res

        return gray_array

    def name(self):
        return "Canny Filter"
