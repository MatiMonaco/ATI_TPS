
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np
import qimage2ndarray
from PyQt5 import QtWidgets,QtCore

class BorderDetectionFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUi()
        self.dy_image = None
        self.dx_image = None

    def setupUi(self):
        self.gradient_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.gradient_groupBox)
        self.gradient_groupBox.setTitle("")
   
        self.gradient_horizontalLayout = QtWidgets.QHBoxLayout(
            self.gradient_groupBox)

        self.btn_dx_gradient = QtWidgets.QPushButton(self.gradient_groupBox)
        self.btn_dy_gradient = QtWidgets.QPushButton(self.gradient_groupBox)
        self.gradient_horizontalLayout.addWidget(self.btn_dx_gradient)
        self.gradient_horizontalLayout.addWidget(self.btn_dy_gradient)
 
        self.gradient_horizontalLayout.setStretch(0,5)
        self.gradient_horizontalLayout.setStretch(1, 5)

        #self.btn_dx_gradient.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&delta;f<sub>x<\></></span></pre></body></html>")
        #self.btn_dy_gradient.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&delta;f<sub>y<\></></span></pre></body></html>")


    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')

        dx_mask = self.generate_dx_mask()
        dy_mask = self.generate_dy_mask()
    
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)

        self.dx_image = self.mask_filtering(
            extended_img, dx_mask, padding_size)
        self.dy_image = self.mask_filtering(
            extended_img, dy_mask, padding_size)

        return np.sqrt(self.dy_image**2 + self.dx_image**2)

       
    def generate_dx_mask(self):
        pass
    def generate_dy_mask(self):
        pass