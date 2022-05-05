from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math
from filters.feature_extraction.hough_transform import HoughTransform


# Override la funcion del circle
class HoughTransformCircle(HoughTransform):

    def __init__(self, update_callback):

        self.a_param = {
            "param_name": "center_x", 
            "min": 5,
            "max": 10, 
            "parts": 25
        } 

        self.b_param = {
            "param_name": "center_y", 
            "min": 5,
            "max": 10, 
            "parts": 25
        }

        self.radius_param = {
            "param_name": "radius", 
            "min": -90,
            "max": 90, 
            "parts": 25
        }
        super().__init__(update_callback)

    def accumulate(self,x,y):

        for i in range(self.param_values_len[0]):
            a = self.param_values[0][i]
            for j in range(self.param_values_len[1]):
                b = self.param_values[1][j]
                for k in range(self.param_values_len[2]):
                    radius = self.param_values[2][k]
                    dist_to_circle = self.calculate_distance_to_circle(x,y,a,b,radius)
                    if dist_to_circle < self.epsilon:
                        self.accumulator[i,j] +=1


    def calculate_distance_to_circle(self,x,y,a,b,radius):
        # (x-a)**2 + (y-b)**2 = radius**2
        return abs(radius**2 - (x-a)**2 - (y-b)**2)
