from itertools import accumulate
from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math


class HoughTransform():

    def __init__(self, params):
         
        self.params = params
        self.params_len = len(self.params)

        self.border_detection_filter  = None
        self.umbralization_filter = None
        self.epsilon = 0.1


    def apply(self, img):
        self.border_detection_filter.channels = self.channels
        border_image = self.border_detection_filter.apply(img)
        self.umbralization_filter.channels = self.channels
       
        
        # Espacio de parametros en la matriz acumulador 
         
        accumulator = self.calculate_accumulator() # La matriz acumulador A tiene la misma dimension en la que se decide discretizar el espacio de par´ametros. La celda A(i, j) corresponde a las coordenadas del espacio de params (ai, bj)

        #Para cada elemento (ai, bj) y para cada pixel (xk , yk ) blanco, sumarle al accum
 
    def calculate_distance_to_figure(self,x,y):
        pass

    def figure_equation(self): 
        pass

    def calculate_accumulator(self):
        param_values_len = list()
        param_values_list = list()
        for i in range(self.params_len):
            min = self.params[i]['min']
            max = self.params[i]['max']
            parts =  self.params[i]['parts']
            param_values = list(np.linspace(min,max, parts))
            print(f"param {self.params[i]['param_name']} values: {param_values}")
            param_values_len.append(len(param_values))  
            param_values_list.append(param_values) # estos son los posibles valores que puede tomar ese param
        
        accumulate =  np.zeros(tuple(param_values_len))
        param_values_len.append(self.params_len)
        print("acummulate: ",accumulate.shape)
        param_values  =np.zeros(param_values_len)
        print("param values: ",self.param_values.shape)
        return accumulate
               