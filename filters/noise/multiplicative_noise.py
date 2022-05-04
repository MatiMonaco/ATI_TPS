from PyQt5.QtGui import QPixmap
from .noise import Noise
import qimage2ndarray
import numpy as np
import math


class MultiplicativeNoise(Noise):

    def __init__(self, update_callback):
        super().__init__(update_callback)

    def setupUI(self):
        super().setupUI()

    def apply(self, img_arr):

        img_arr = img_arr.astype("float64")
        width = img_arr.shape[1]
        height =  img_arr.shape[0]
       
        total_pixels = width*height
    
        pixel_proportion = math.floor(total_pixels * self.density)
     

        x, y = self.generateRandomCoords(width, height, pixel_proportion)

        self.noises = self.generateNoise(pixel_proportion)
         
        noises = self.noises[np.newaxis].T
        
            
        img_arr[x, y] *=  noises
      

        for channel in range(0,self.channels):
            max = np.max(img_arr[:,:,channel])
            min = np.min(img_arr[:, :, channel])
            
            interval = max-min
            
            img_arr[:, :, channel] = 255 * \
                ((img_arr[:, :, channel] - min) / interval)

        return img_arr

    def generateNoise(self, size):
        pass
