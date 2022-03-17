from PyQt5.QtGui import QPixmap
from .noise import Noise
import qimage2ndarray
import numpy as np
import math


class AdditiveNoise(Noise):

    def __init__(self, update_callback):
        super().__init__(update_callback)

    def setupUI(self):
        super().setupUI()

    def applyNoise(self, pixmap, density):

        img = pixmap.toImage()
        width = img.width
        height = img.height
        total_pixels = width*height
        pixel_proportion = math.floor(total_pixels * density)

        x, y = self.generateRandomCoords(width*height, width)

        noises = self.generateNoise(pixel_proportion)[np.newaxis].T

        img_arr = qimage2ndarray.rgb_view(img).astype('float64')

        img_arr[x, y] += noises

        max = np.max(img_arr)
        min = np.min(img_arr)
        interval = min-max

        img_arr[x, y] = 255*(img_arr[x, y] - min) / interval

        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def generateNoise(self, size):
        pass
