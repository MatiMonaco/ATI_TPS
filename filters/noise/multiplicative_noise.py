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
        print(f"w: {width}, h : {height}")
        total_pixels = width*height
        print("density: ", self.density)
        pixel_proportion = math.floor(total_pixels * self.density)
        print(f"pixel proportion: {pixel_proportion}")

        x, y = self.generateRandomCoords(width, height, pixel_proportion)

        self.noises = self.generateNoise(pixel_proportion)
        noises = self.noises[np.newaxis].T
        

        img_arr = qimage2ndarray.rgb_view(img).astype('float64')

        img_arr[x, y] *= noises
        print(noises)
        print(img_arr)

        for color in range(0,3):
            max = np.max(img_arr[:,:,color])
            min = np.min(img_arr[:,:,color])
            interval = max-min
            img_arr[:,:,color] = 255*((img_arr[:,:,color] - min) / interval)
             
            print(interval)
        
        print(img_arr)

        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def generateNoise(self, size):
        pass
