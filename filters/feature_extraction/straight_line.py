from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math
from feature_extraction.hough_transform import HoughTransform

# Override la funcion de la recta

class HoughTransformStraightLine(HoughTransform):

    def __init__(self, update_callback):
        super().__init__(update_callback)