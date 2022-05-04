import numpy as np
from filters.filter import Filter

import math

class HoughTransform(Filter):

    def __init__(self,update_callback):
        super().__init__()
        self.update_callback = update_callback
        self.params = None
        self.params_len = None
        self.param_values = None
        self.param_values_len = None

        self.border_detection_filter  = None
        self.umbralization_filter = None
        self.epsilon = 0.1

        self.accumulator = None

        self.accumulated_percentage = 0.8

    def set_parameters(self):
        pass

    def apply(self, img_arr):
        # self.border_detection_filter.channels = self.channels
        # edges_image = self.border_detection_filter.apply(img_arr)
        # self.umbralization_filter.channels = self.channels
        # edges_image = self.umbralization_filter.apply(img_arr)
    
        # Creo matriz acumuladora
        if self.accumulator is None:
            self.accumulator = self.calculate_accumulator() # La matriz acumulador A tiene la misma dimension en la que se decide discretizar el espacio de par´ametros. La celda A(i, j) corresponde a las coordenadas del espacio de params (ai, bj)

        #Para cada elemento (ai, bj) y para cada pixel (xk , yk ) blanco, sumarle al accum
        edge_pixels = np.argwhere(img_arr == 255) # las posiciones de los pixels blancos
        for edge_pixel_coords in edge_pixels:
            self.accumulate(edge_pixel_coords[1],edge_pixel_coords[0])

        # Examinar el contenido de las celdas del acumulador con altas concentraciones
        accum_quantity = math.floor(np.prod(self.param_values_len)*self.accumulated_percentage) # TODO check
        figure_params_indexes = self.top_n_indexes(self.accumulator,accum_quantity)

        # Dibujar  figuras TODO 

        final_img =  self.draw_figure(edges_image, figure_params_indexes)
        print(f"final img = {final_img}")
        return final_img

    def top_n_indexes(arr, n):
        idx = np.argpartition(arr, arr.size-n, axis=None)[-n:]
        width = arr.shape[1]
        return [divmod(i, width) for i in idx]    
 
    def accumulate(self,x,y):
        pass

    def draw_figure(self, img_arr, lines): 
        pass
    

    def calculate_accumulator(self):
      
        self.param_values = list()
        self.param_values_len = list()
    
        for i in range(self.params_len):
            min = self.params[i]['min']
            max = self.params[i]['max']
            parts =  self.params[i]['parts']
            param_values = list(np.linspace(min,max, parts))
            print(f"param {self.params[i]['param_name']} values: {param_values}")
            self.param_values_len.append(len(param_values))   # TODO check que la matrix sea de partsxparts
            self.param_values.append(param_values) # estos son los posibles valores que puede tomar ese param
        
        accumulate =  np.zeros(tuple(self.param_values_len))
    
        print("acummulate: ",accumulate.shape)
    
        return accumulate
    
    