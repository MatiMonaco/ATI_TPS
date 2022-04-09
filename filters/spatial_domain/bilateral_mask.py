from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QDoubleValidator
import qimage2ndarray
import numpy as np
import math


class BilateralMask(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUi()
        self.sigmaS = 2  # constante de suavizado en términos espaciales
        self.sigmaR = 30 # constante de suavizado en términos de intensidad de color

    def generate_mask(self, sub_img, mask_size): 
        
        center = int(math.floor(mask_size/2))
        mask = []
        sum = 0
        for k in range(mask_size):
            mask.append([])
            for l in range(mask_size):
                # print(f"exp: {-((center-k)**2 + (center-l)**2 / (2 * self.sigmaS**2)) - (np.linalg.norm(sub_img[center,center] - sub_img[k,l])**2 / (2 * self.sigmaR**2))}")
                blur =  ((center-k)**2 + (center-l)**2) / (2 * self.sigmaS**2)
                intensity = np.linalg.norm(sub_img[center,center] - sub_img[k,l])**2 / (2 * self.sigmaR**2)
                e = math.exp( - blur - intensity) 
                
                sum += e
                mask[k].append(e)
        # print(f"sum is: {sum}, mask without sum: {mask}")
        return np.array(mask) / sum

    def apply_mask(self, sub_img, mask=None):
        mask = self.generate_mask(sub_img, self.mask_size)
        # print(f"mask: {mask}")
        return super().apply_mask(sub_img, mask)
     
         
        
    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
        self.mask_size = 7
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)

        return self.mask_filtering(extended_img, None ,padding_size)

    #############################################################################################################        
    def name(self):
        return "Bilateral Mask Filter"
        
    def setupUi(self):
        pass
    