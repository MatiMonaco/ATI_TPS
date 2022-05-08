from PyQt5.QtGui import QPixmap 

from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
from enum import Enum
import numpy as np

import qimage2ndarray
import numpy as np
import math

class PixelType(Enum): 
    CORNER = [255,0,0]
    EDGE = [0,0,255]
    COMMON = 1

class Susan(SpatialDomainFilter):

    

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.mask_size = 7 
        self.threshold = 15
        self.setupUI()

    def setupUI(self):
        super().setupUI()

    
        
    def generate_mask(self,mask_size): 
        mask = np.zeros((mask_size, mask_size))
        middle = math.floor(mask_size/2)
        # TODO generalizar para todos los tamaños
        mask[middle-3, 2:mask_size-2] = 1 
        mask[middle-2, 1:mask_size-1] = 1 
        mask[middle-1,:]              = 1 
        mask[middle,:]                = 1 
        mask[middle+1,:]              = 1 
        mask[middle+2, 1:mask_size-1] = 1 
        mask[middle+3, 2:mask_size-3] = 1 

        return mask, mask_size

    def apply_mask(self, sub_img, mask=None):
        #Obtener la cantidad de pixeles de la mascara
        total_pixels = mask[mask == 1].size
        central_pixel = sub_img[math.floor(self.mask_size/2), math.floor(self.mask_size/2)] # I(r0)
        pixel_types = []
     
        print("central pixel = ",central_pixel)
        # Aplicar transformacion c(r,r0)
        for channel in range(self.channels):
            neighbours = np.multiply(sub_img[:, :, channel], mask) # I(r)
            total = np.count_nonzero(np.abs(central_pixel[channel] - neighbours) < self.threshold)  # get pixels with similar intensity
            
            pixel_types.append(self.is_edge_or_corner(1 - (total / total_pixels)))
        print("pixel types = ",pixel_types)
        return self.paint_pixel_by_type(pixel_types,central_pixel)
        
        
    def paint_pixel_by_type(self, pixel_types, central_pixel):
        if self.isGrayScale:
            type_ = pixel_types[0]
            if type_ == PixelType.COMMON:
                # print("type common: ",central_pixel)
                return np.ones(3) * central_pixel[0]
            # print("type : ",np.array(type_.value))
            return np.array(type_.value)
        else:
            #TODO: ver que hacer con los channels
            return central_pixel

    def is_edge_or_corner(self, value): 
        threshold = 0.15 
        if np.abs(value - 0.5) < threshold: 
            return PixelType.EDGE
        elif np.abs(value - 0.75) < threshold: 
            return PixelType.CORNER
        else: 
            return PixelType.COMMON 
     


    def name(self):
        return "S.U.S.A.N Filter"
        
    def setupUI(self):
        super().setupUI()