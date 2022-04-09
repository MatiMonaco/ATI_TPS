import numpy as np
import qimage2ndarray
from ..filter import Filter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator


class Difussion(Filter):

    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback
        self.lambda_ = 0.25
        self.iterations = 10


    def apply_difussion(self, img):

        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
        height = img_arr.shape[0]
        width = img_arr.shape[1] 

        for it in range(self.iterations):
            for channel in range(self.channels):
    
                for i in range(width):
                    for j in range(height):

                        curr_pixel = img_arr[i,j, channel]

                        north_deriv = img_arr[i+1,j, channel] - curr_pixel
                        south_deriv = img_arr[i-1,j, channel] - curr_pixel
                        east_deriv  = img_arr[i,j+1, channel] - curr_pixel
                        west_deriv  = img_arr[i,j-1, channel] - curr_pixel

                        img_arr[i,j, channel]+= self.lambda_ * (north_deriv * self.get_kernel(north_deriv, it) +
                                                                south_deriv * self.get_kernel(south_deriv, it) +
                                                                east_deriv  * self.get_kernel(east_deriv,  it) +
                                                                west_deriv  * self.get_kernel(west_deriv,  it))
                    
        return img_arr


    def get_kernel(self,deriv, sigma):

        pass







