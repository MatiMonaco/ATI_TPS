from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math


class HoughTransform():

    def __init__(self, update_callback):
        super().__init__(update_callback)


    def apply(self, img):
        width = img.width()
        height = img.height()

