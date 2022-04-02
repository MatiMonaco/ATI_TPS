
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np
import qimage2ndarray
from PyQt5 import QtWidgets,QtCore
import matplotlib.pyplot as plt
class GradientFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUi()
        self.dy_image = None
        self.dx_image = None

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
        fig,(ax1, ax2) = plt.subplots(1,2, sharey=True)
        ax1.imshow(self.dy_image.astype('int32'))
        ax1.set_title("Horizontal Borders")
        ax2.imshow(self.dx_image.astype('int32'))
        ax2.set_title("Vertical Borders")
        plt.show()

    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')

        dx_mask = self.generate_dx_mask()
        dy_mask = self.generate_dy_mask()
    
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)

        # La mascara en x me detecta borders verticales
        self.dy_image = self.mask_filtering(
            extended_img, dx_mask, padding_size)
        
        # La mascara en y me detecta borders horizontales
        self.dx_image = self.mask_filtering(
            extended_img, dy_mask, padding_size)
       
        
        border_magnitude = np.sqrt(self.dy_image**2 + self.dx_image**2)     
        
        return self.normalizeIfNeeded(border_magnitude)

       
    def generate_dx_mask(self):
        pass
    
    def generate_dy_mask(self):
        pass