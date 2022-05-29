from dis import dis
import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.filters import threshold_multiotsu

from filters.filter import Filter
from PyQt5 import QtWidgets, QtCore

from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter 
from filters.spatial_domain.gauss_mask import GaussMaskFilter 

class Harris(Filter):


    def __init__(self, update_callback, setupUI = True):
        super().__init__()
        self.update_callback = update_callback
        self.sobel_filter = SobelFilter(update_callback)

        self.prewitt_filter = PrewittFilter(update_callback)
        self.current_filter = self.sobel_filter
        
        if setupUI:
            self.setupUI()

    def apply(self, img_arr):
   
        self.current_filter.channels = self.channels

        # 1. Se calculan las derivadas de Prewitt o Sobel      
        self.edge_magnitude_image = self.current_filter.apply(img_arr)
        self.dx_image, self.dy_image = self.current_filter.get_gradient() # la de 0 verticales tiene que ser Ix
      
        # 2. Suavizar con Gauss
        dx2,dy2, dxy = self.apply_gauss_mask()

        # 3. Calcular valor de respuesta de Harris
        response = self.calculate_response(dx2, dy2, dxy)

        # 4. Buscar los maximos 
        edges = self.get_max_values()

        # 5. Retorno imagen con los edges pintados.


    def apply_gauss_mask(self): 

        dx2 = np.linalg.matrix_power(self.dx_image, 2) # chequear que esto sea elemento a elemento
        dy2 = np.linalg.matrix_power(self.dy_image, 2) 

        # Aplico Gauss 7x7 sigma=2 
        dx2_gauss = GaussMaskFilter.apply(dx2) # TODO que retorne y que se le puedan setear la mask y sigma
        dy2_gauss = GaussMaskFilter.apply(dy2)
        dxy_gauss =  GaussMaskFilter.apply(self.edge_magnitude_image) # esto es Ix*Iy punto a punto, sin suavizar

        return dx2_gauss, dy2_gauss, dxy_gauss
        
    def calculate_response(self, dx2, dy2, dxy): 
        k = 0.04
        return (dx2*dy2 - dxy**2) - k * (dx2+dy2)**2

    def get_max_values(response): 
        # Response es una matriz de numeros, los pixeles que tengan mayor response se corresponden con las esquinas (entiendo que se corresponden por indice)
        pass


    def setupUI(self):

        pass