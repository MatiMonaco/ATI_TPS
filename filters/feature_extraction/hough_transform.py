from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math


class HoughTransform():

    def __init__(self, params):
         
        self.params = params 


    def apply(self, img):
    # Previamente pasar un edge_detector y umbralizar, después se aplica la transformacoion de Hough
    # param1 = {
    #   "param_name": "rho", 
    #   "min": 4,
    #   "max": 5, 
    #   "parts": 10  para discretizar 
    #}
       
        
        # Espacio de parametros en la matriz acumulador 
         
        accumulator = self.calculate_accumulator() # La matriz acumulador A tiene la misma dimension en la que se decide discretizar el espacio de par´ametros. La celda A(i, j) corresponde a las coordenadas del espacio de params (ai, bj)

        #Para cada elemento (ai, bj) y para cada pixel (xk , yk ) blanco, sumarle al accum
 

    def figure_equation(self): 
        pass

    def calculate_accumulator(self):
        pass