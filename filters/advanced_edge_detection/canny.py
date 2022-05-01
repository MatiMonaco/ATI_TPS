from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math

from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter


class Canny():

    def __init__(self, update_callback): 

        pass


    def apply(self, img):
        width = img.width()
        height = img.height()
        # 1. Suavizamiento y diferenciación --> es pasarle la mask de Gauss pero NO hay que hacerlo!! 
        # 2. Obtener la dirección perpendicular al borde (aplicar sobel o prewitt)
        edge_magnitude_image, dx_image, dy_image = PrewittFilter.apply(img) # TODO parametrizar para que sea sobel o prewitt y que retornen tmb dx y dy (ahora solo retornan la sintesis y encima ya normalizada, creo que hay que manejarla sin normalizar todavia aca)

        # 3. Ángulo del gradiente para estimar la direccion ortogonal al borde
        direction_angle = self.discretize_angle(np.arctan(dy_image/ dx_image)) if dx_image != 0 else 90

        # 4. Supresión de no máximos
        self.no_max_supression(edge_magnitude_image, direction_angle)

        # 5. Umbralización con histéresis
        
                 


    def discretize_angle(self,angle): 
        # TODO CREO que angle tmb puede ser negativo, a chequear
        if (angle >= 0 and angle <= 22.5) or (angle >= 157.5 and angle <= 180): 
            discretized_angle = 0
        
        elif angle > 22.5 and angle <= 67.5:
            discretized_angle = 45 
        
        elif angle > 67.5 and angle <= 112.5:
            discretized_angle = 90
        
        else: 
            discretized_angle = 135 

        return discretized_angle

    def no_max_supression(self, edge_magnitude_image, direction): 

        for row in edge_magnitude_image.shape[1]: # TODO ojo con cual es el height y el width que la pifeo siempre
            for col in edge_magnitude_image.shape[0]:

                curr_pixel = edge_magnitude_image[col, row] # Para cada pixel con magnitud de borde no cero, inspeccionar los pixels adyacentes indicados en la dirección ortogonal al su borde.
                if curr_pixel != 0:                     
                    adjacent_pixels = self.get_adjacent_pixels(curr_pixel, direction)

                    # Si la magnitud de cualquiera de los dos pixels adyacentes es mayor que la del pixel en cuestión, entonces borrarlo como borde.
        
    def get_adjacent_pixels(self, curr_pixel, direction):
        pass


