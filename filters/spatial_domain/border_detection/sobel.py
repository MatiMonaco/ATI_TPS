
from filters.spatial_domain.border_detection.border_detection_filter import BorderDetectionFilter
import numpy as np
import qimage2ndarray
from PyQt5 import QtWidgets,QtCore

class SobelFilter(BorderDetectionFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUi()

    def generate_dx_mask(self):
        return np.array([
                        [-1,-2,-1],
                        [0, 0, 0],
                        [1, 2, 1]])
    
    def generate_dy_mask(self):
        return np.array([
                        [-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])