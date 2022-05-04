from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math
from feature_extraction.hough_transform import HoughTransform

# Override la funcion de la recta

class HoughTransformStraightLine(HoughTransform):

    def __init__(self, update_callback):
        super().__init__(update_callback)

        param1 = {
            "param_name": "rho", 
            "min": 5,
            "max": 10, 
            "parts": 10
        } 

        param2 = {
            "param_name": "rho", 
            "min": 5,
            "max": 10, 
            "parts": 10
        }

        self.params = [param1, param2]
    
    # def calculate_accumulator(self): 

    #     min_a = self.params[0]['min']
    #     max_a = self.params[0]['max']
    #     parts_a =  self.params[0]['parts']

    #     min_b = self.params[1]['min']
    #     max_b = self.params[1]['max']
    #     parts_b =  self.params[1]['parts']
    #     print(list(np.linspace(min,max, parts_a))) # estos son los posibles valores que puede tomar ese param 

    #     accumulator = np.zeros(parts_a, parts_b) 

    #     return accumulator


