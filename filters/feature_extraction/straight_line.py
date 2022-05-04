from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math
from feature_extraction.hough_transform import HoughTransform

# Override la funcion de la recta

class HoughTransformStraightLine(HoughTransform):

    def __init__(self, update_callback):
        self.rho_param = {
            "param_name": "rho", 
            "min": -10,
            "max": 10, 
            "parts": 25
        } 

        self.theta_param = {
            "param_name": "theta", 
            "min": -180,
            "max": 180, 
            "parts": 25
        }
        super().__init__(update_callback,[self.theta_param, self.rho_param])

    def accumulate(self,x,y):

        for i in range(self.params_len[0]):
            theta = self.param_values[0][i]
            for j in range(self.params_len[1]):
                rho = self.param_values[1][j]
                dist_to_line = self.calculate_distance_to_line(x,y,theta,rho)
                if dist_to_line < self.epsilon:
                    self.accumulator[i,j] +=1


    def calculate_distance_to_line(self,x,y,theta,rho):
        # y*sen(theta) + x*cos(theta) = rho
        return abs(rho - x*math.cos(theta) - y*math.sin(theta))


