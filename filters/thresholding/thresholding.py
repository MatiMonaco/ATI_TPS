
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np
import qimage2ndarray
import math
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QIntValidator


class Thresholding():


    def __init__(self, update_callback):
        super().__init__(update_callback)
  
        
    def get_threshold(self, img_arr):

        
        threshold = np.mean(img_arr)            # intial T (0;255) = img mean  
        delta_threshold = math.inf

        while delta_threshold > 1:              # iterate until deltaT < 1
            white_pixels = []
            black_pixels = []
        
            for pixel in img_arr:
                if pixel < threshold:         
                    black_pixels.append(pixel)  # pixels that are going to be black, not yet.
                else:  
                    white_pixels.append(pixel)  # pixels that are going to be white

            white_mean = np.mean(white_pixels)
            black_mean = np.mean(black_pixels)

            new_threshold = (white_mean+black_mean)/2    

            delta_threshold = new_threshold - threshold
            threshold = new_threshold
        
        return threshold
    
    def global_thresholding(self, img): 
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')

        threshold = self.get_threshold(img_arr)

        height = img_arr.shape[0]
        width = img_arr.shape[1]  


        for channel in range(self.channels):
            for x in range(height):
                for y in range(width):
                  
                    if img_arr[x,y,channel] < threshold:         
                        img_arr[x,y,channel] = 0   
                    else:  
                        img_arr[x,y,channel] = 255
        
        return img_arr