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

    def applyNoise(self, pixmap, density):

        img = pixmap.toImage()
        width = img.width()
        height = img.height()
        print(f"w: {width}, h : {height}")
        total_pixels = width*height
        print("density: ", density)
        pixel_proportion = math.floor(total_pixels * density)
        print(f"pixel proportion: {pixel_proportion}")

        x, y = self.generateRandomCoords(width, height, pixel_proportion)

        noises = self.generateNoise(pixel_proportion)[np.newaxis].T

        img_arr = qimage2ndarray.rgb_view(img).astype('float64')

        img_arr[x, y] *= noises

        max = np.max(img_arr)
        min = np.min(img_arr)
        interval = max-min

        img_arr[x, y] = 255*(img_arr[x, y] - min) / interval

        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def generateNoise(self, size):
        pass
