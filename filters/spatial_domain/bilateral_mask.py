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
        self.sigmaS = 1
        self.sigmaR = 1
        
    def name(self):
        return "Bilateral Mask Filter"
        
    def setupUi(self):
        pass
    
    def generate_mask(self, sub_img, mask_size): 
        
        center = int(math.floor(mask_size/2))
        mask = []
        for k in range(mask_size):
            mask.append([])
            for l in range(mask_size):
                
                mask[k].append(math.exp((-(center-k)**2 + (center-l)**2 / 2 * self.sigmaS**2) - np.linalg.norm(sub_img[center,center] - sub_img[k,l]) / 2 * self.sigmaR**2))
        return 1/(self.sigma * np.sqrt(2 * np.pi)) * np.exp( - (np.array(mask) - self.mu)**2 / (2 * self.sigma**2)), mask_size


    def apply_mask(self, sub_img, mask=None):

        pixels_by_channel = []
        mask = self.generate_mask(sub_img, self.mask_size)
        for channel in range(0, self.channels):
            pixels_by_channel.append(
                np.sum(np.multiply(sub_img[:, :, channel], mask)))

        return np.array(pixels_by_channel)
        
    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)

        return self.mask_filtering(extended_img, padding_size)