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

    def apply(self, img):

      
        width = img.width()
        height = img.height()
       
        total_pixels = width*height
    
        pixel_proportion = math.floor(total_pixels * self.density)
     

        x, y = self.generateRandomCoords(width, height, pixel_proportion)

        self.noises = self.generateNoise(pixel_proportion)
        print(f"nosies: ", self.noises[:100])
        noises = self.noises[np.newaxis].T
        

        img_arr = qimage2ndarray.rgb_view(img).astype('float64')
        max = np.max(img_arr[:, :, 0])
        min = np.min(img_arr[:, :, 0])
        print(f"Antes R min: {min}, max: {max}")
        max = np.max(img_arr[:, :, 1])
        min = np.min(img_arr[:, :, 1])
        print(f"Antes G min: {min}, max: {max}")
        max = np.max(img_arr[:, :, 2])
        min = np.min(img_arr[:, :, 2])
        print(f"Antes B min: {min}, max: {max}")
        img_arr[x, y] *= noises
      

        for color in range(0,self.channels):
            max = np.max(img_arr[:,:,color])
            min = np.min(img_arr[:,:,color])
            
            interval = max-min
            print(f"Despues min: {min}, max: {max}, interval: {interval}")
            img_arr[:,:,color] = 255*((img_arr[:,:,color] - min) / interval)

        return img_arr

    def generateNoise(self, size):
        pass
