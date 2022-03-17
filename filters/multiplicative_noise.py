from PyQt5.QtGui import QPixmap
from .noise import Noise
import qimage2ndarray
import numpy as np

class MultiplicativeNoise(Noise):

    def __init__(self,update_callback):
        super().__init__(update_callback)

    def applyNoise(self, pixmap, density):
      
        print(f"APPLY TRHESHOLD: {self.threshold}")
        img = pixmap.toImage()
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
      
       
        for i in img_arr.width():
            for j in img_arr.height():
                if np.random.default_rng().normal(0, 1) < density:
                    noise = self.generateNoise()
                    img_arr[i,j] *= noise
                   
        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def generateNoise(self):
        pass
