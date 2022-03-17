from PyQt5.QtGui import QPixmap
from .noise import Noise
import qimage2ndarray
import numpy as np

class MultiplicativeNoise(Noise):

    def __init__(self,update_callback):
        super().__init__(update_callback)

    def setupUI(self):
        super().setupUI()

    def applyNoise(self, pixmap, density):
      
      
        img = pixmap.toImage()
        img_arr = qimage2ndarray.rgb_view(img).astype('float64')
      
        for i in range(img.width()):
            print(i)
            for j in range(img.height()):
                print(j)
                if np.random.default_rng().normal(0, 1) < density:
                    noise = self.generateNoise()
                    img_arr[i, j] *= noise
                   
        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def generateNoise(self,size):
        pass
