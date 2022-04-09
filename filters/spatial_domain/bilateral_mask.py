from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QDoubleValidator
import qimage2ndarray
import numpy as np
import math


class BilateralMask(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
       
        self.sigmaS = 3.0  # constante de suavizado en términos espaciales
        self.sigmaR = 30.0 # constante de suavizado en términos de intensidad de color
        self.mask_size = 7
        self.setupUI()


    def setupUI(self):
        super().setupUI()
        
        self.bilateral_horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.bilateral_horizontalLayout)
        self.sigma_s_label = QtWidgets.QLabel(self.spatial_domain_groupBox)
        self.sigma_s_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.sigma_s_label.setScaledContents(False)
        self.sigma_s_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sigma_s_line_edit = QtWidgets.QLineEdit(self.spatial_domain_groupBox)
        self.bilateral_horizontalLayout.addWidget(self.sigma_s_label)
        self.bilateral_horizontalLayout.addWidget(self.sigma_s_line_edit)

        self.bilateral_horizontalLayout.addItem( QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.sigma_r_label = QtWidgets.QLabel(self.spatial_domain_groupBox)
        self.sigma_r_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.sigma_r_label.setScaledContents(False)
        self.sigma_r_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sigma_r_line_edit = QtWidgets.QLineEdit(self.spatial_domain_groupBox)
        self.bilateral_horizontalLayout.addWidget(self.sigma_r_label)
        self.bilateral_horizontalLayout.addWidget(self.sigma_r_line_edit)

        self.bilateral_horizontalLayout.addItem( QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.bilateral_horizontalLayout.setStretch(0, 1)
        self.bilateral_horizontalLayout.setStretch(1, 1)
        self.bilateral_horizontalLayout.setStretch(2, 2)
        self.bilateral_horizontalLayout.setStretch(3, 1)
        self.bilateral_horizontalLayout.setStretch(4, 1)
        self.bilateral_horizontalLayout.setStretch(5, 1)


        self.sigma_s_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&sigma;<sub>s</></></span></pre></body></html>")
        self.sigma_r_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&sigma;<sub>r</></></span></pre></body></html>")

        self.onlyDouble = QDoubleValidator()
        self.onlyDouble.setBottom(0)
        self.sigma_s_line_edit.setValidator(self.onlyDouble)
        self.sigma_r_line_edit.setValidator(self.onlyDouble)

        self.sigma_s_line_edit.textChanged.connect(self.setSigmaS)
        self.sigma_r_line_edit.textChanged.connect(self.setSigmaR)

        self.sigma_s_line_edit.setText(str(self.sigmaS))
        self.sigma_r_line_edit.setText(str(self.sigmaR))
      

    def setSigmaS(self, text):
        if text != '':
            self.sigmaS = float(text)

    def setSigmaR(self, text):
        if text != '':
            self.sigmaR = float(text)
        

    def generate_mask(self, sub_img, mask_size): 
        #print("sum_img size: ",sub_img.shape)
        center = int(math.floor(mask_size/2))
        mask = []
        sum = 0
        for k in range(mask_size):
            mask.append([])
            for l in range(mask_size):
              
                blur =  ((center-k)**2 + (center-l)**2) / (2 * self.sigmaS**2)
              
                intensity = (np.linalg.norm(sub_img[center,center] - sub_img[k,l])**2) / (2 * self.sigmaR**2)
                e = math.exp( - blur - intensity) 
                
                sum += e
    
                mask[k].append(e)
       
        # print(f"sum is: {sum}, mask without sum: {mask}")
        return np.array(mask) / sum

    def apply_mask(self, sub_img, mask=None):
        mask = self.generate_mask(sub_img, self.mask_size)
        #print(f"mask: {mask}")
        return super().apply_mask(sub_img, mask)

     
        
    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')[:,:,0:self.channels]
        print("img_ARR: ",img_arr.shape)
        print("mask size. ",self.mask_size)
        
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)
        print("extended: ",extended_img.shape)

        return self.mask_filtering(extended_img, None ,padding_size)

    #############################################################################################################        
    def name(self):
        return "Bilateral Mask Filter"
    
      

    def setSigmaS(self, text):
        if text != '':
            self.sigmaS = float(text)

    def setSigmaR(self, text):
        if text != '':
            self.sigmaR = float(text)
        

    def generate_mask(self, sub_img, mask_size): 
        #print("sum_img size: ",sub_img.shape)
        center = int(math.floor(mask_size/2))
        mask = []
        sum = 0
        for k in range(mask_size):
            mask.append([])
            for l in range(mask_size):
              
                blur =  ((center-k)**2 + (center-l)**2) / (2 * self.sigmaS**2)
              
                intensity = (np.linalg.norm(sub_img[center,center] - sub_img[k,l])**2) / (2 * self.sigmaR**2)
                e = math.exp( - blur - intensity) 
                
                sum += e
    
                mask[k].append(e)
       
        # print(f"sum is: {sum}, mask without sum: {mask}")
        return np.array(mask) / sum

    def apply_mask(self, sub_img, mask=None):
        mask = self.generate_mask(sub_img, self.mask_size)
        #print(f"mask: {mask}")
        return super().apply_mask(sub_img, mask)

     
        
    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')[:,:,0:self.channels]
        print("img_ARR: ",img_arr.shape)
        print("mask size. ",self.mask_size)
        
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)
        print("extended: ",extended_img.shape)

        return self.mask_filtering(extended_img, None ,padding_size)

    #############################################################################################################        
    def name(self):
        return "Bilateral Mask Filter"
        
    def setupUi(self):
        pass
    