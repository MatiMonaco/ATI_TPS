from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np
import qimage2ndarray
from PyQt5 import QtWidgets,QtCore
import matplotlib.pyplot as plt

class DirectionalFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUi()
        self.dy_image = None
        self.dx_image = None
        self.left_diag = None
        self.right_diag = None 

    def setupUi(self):
        self.gradient_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.gradient_groupBox)
        self.gradient_groupBox.setTitle("")
   
        self.gradient_horizontalLayout = QtWidgets.QHBoxLayout(self.gradient_groupBox)

        self.btn_directional_gradient = QtWidgets.QPushButton(self.gradient_groupBox)
       
        self.gradient_horizontalLayout.addWidget(self.btn_directional_gradient)

        self.btn_directional_gradient.setText("Show Directional Borders")
        self.btn_directional_gradient.clicked.connect(self.show_directional_borders)
    

    def show_directional_borders(self):
        fig,axes = plt.subplots(2,2, sharey=True)
        axes[0,0].imshow(self.dy_image.astype('int32'))
        axes[0,0].set_title("Horizontal Borders")
        axes[0,1].imshow(self.dx_image.astype('int32'))
        axes[0,1].set_title("Vertical Borders")
        axes[1,0].imshow(self.left_diag_image.astype('int32'))
        axes[1,0].set_title("Left Diagonal Borders")
        axes[1,1].imshow(self.right_diag_image.astype('int32'))
        axes[1,1].set_title("Right Diagonal Borders")
        plt.show()

    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')

        dx_mask = self.generate_dx_mask()
        dy_mask = self.generate_dy_mask()
        left_diag_mask = self.generate_left_diag_mask()
        right_diag_mask = self.generate_right_diag_mask()
    
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)

        self.dx_image = self.mask_filtering(
            extended_img, dx_mask, padding_size)
        
        self.dy_image = self.mask_filtering(
            extended_img, dy_mask, padding_size)
       
        self.left_diag_image = self.mask_filtering(
            extended_img, left_diag_mask, padding_size)
        
        self.right_diag_image = self.mask_filtering(
            extended_img, right_diag_mask, padding_size)
        
        border_magnitude = np.sqrt(self.dy_image**2 + self.dx_image**2 +  self.left_diag_image**2 +  self.right_diag_image**2) # TODO preguntar     
        
        return self.normalizeIfNeeded(border_magnitude)

       
    def generate_dx_mask(self):
        return np.array([
                        [-1 , 1 ,1],
                        [-1 , -2 ,1],
                        [-1 , 1 ,1]])
    
    def generate_dy_mask(self):
        return np.array([
                        [1 , 1 ,1],
                        [1 , -2 ,1],
                        [-1 , -1 ,-1]])

    def generate_left_diag_mask(self):
        return np.array([
                        [1,     1,     1],  # \
                        [-1,   -2,     1],  #   \
                        [-1,   -1,     1]]) #     \

    def generate_right_diag_mask(self):
        return np.array([
                        [-1,    -1,     1],  #      /
                        [-1,    -2,     1],  #    /
                        [1,      1,     1]]) #  /