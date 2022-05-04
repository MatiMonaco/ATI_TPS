
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np
import qimage2ndarray
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import math
class GradientFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUI()
        self.dy_image = None
        self.dx_image = None

    

    def setupUI(self):
      
        self.gradient_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.gradient_groupBox)
        self.gradient_groupBox.setTitle("")
   
        self.gradient_horizontalLayout = QtWidgets.QHBoxLayout(self.gradient_groupBox)

        self.btn_directional_gradient = QtWidgets.QPushButton(self.gradient_groupBox)
       
        self.gradient_horizontalLayout.addWidget(self.btn_directional_gradient)

        self.btn_directional_gradient.setText("Show Directional Borders")
        self.btn_directional_gradient.clicked.connect(self.show_directional_borders)
 
    def correct_if_gray(self, gray_array):
        if gray_array.shape[2] == 1:
           res = np.empty((gray_array.shape[0], gray_array.shape[1], 3))
           res[:, :, 0:3] = gray_array
           return res

        return gray_array

    def show_directional_borders(self):
        plt.ion()
        fig,(ax1, ax2) = plt.subplots(1,2, sharey=True)

        dy_image = self.correct_if_gray(self.dy_image)
        dx_image = self.correct_if_gray(self.dx_image)

        ax1.imshow(dy_image.astype('int32'))
        ax1.set_title("Vertical Borders")
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax2.imshow(dx_image.astype('int32'))
        ax2.set_title("Horizontal Borders")
        ax2.set_yticklabels([])
        ax2.set_xticklabels([])
        plt.show()

    def apply(self, img_arr):
        dx_mask = self.generate_dx_mask()
        dy_mask = self.generate_dy_mask()
    
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)

        # La mascara en x me detecta borders verticales
        self.dy_image = self.mask_filtering(
            extended_img, dx_mask, padding_size,norm=False)
        
        # La mascara en y me detecta borders horizontales
        self.dx_image = self.mask_filtering(
            extended_img, dy_mask, padding_size,norm=False)
       
        edge_magnitude = np.sqrt(self.dy_image**2 + self.dx_image**2)     
        #edge_magnitude = abs(self.dy_image) + abs(self.dx_image)     
        return edge_magnitude

    def get_gradient(self):
        return self.dx_image,self.dy_image

       
    def generate_dx_mask(self):
        pass
    
    def generate_dy_mask(self):
        pass