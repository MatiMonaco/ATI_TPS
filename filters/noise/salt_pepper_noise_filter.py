from .noise import Noise
from PyQt5.QtGui import QPixmap
import qimage2ndarray
import numpy as np
import math


class SaltPepperNoiseFilter(Noise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.p0 = 0.5
        self.p1 = 1 - self.p0

        self.saltPepearArr = np.vectorize(self.saltPepear)

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

        img_arr = qimage2ndarray.rgb_view(img).astype('int32')

        img_arr[x, y] -= img_arr[x, y]
        img_arr[x, y] += noises

        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def saltPepear(self, x):
        if x <= self.p0:
            return 0
        elif x >= self.p1:
            return 1

    def generateNoise(self, size):
        x = np.random.uniform(size=size)
        return self.saltPepearArr(x)*255
