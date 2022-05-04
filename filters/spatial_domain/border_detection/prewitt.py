from filters.spatial_domain.border_detection.gradient_filter import GradientFilter
import numpy as np

class PrewittFilter(GradientFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
      
    def name(self):
        return "Prewitt Filter"

    def generate_dx_mask(self):
        return np.array([
                        [-1 , 0 ,1],
                        [-1 , 0 ,1],
                        [-1 , 0 ,1]])
    
    def generate_dy_mask(self):
        return np.array([
                        [-1,-1,-1],
                        [0 , 0, 0],
                        [1 , 1, 1]])

    def apply(self,img_arr):
        edge_magnitude = super().apply(img_arr)
    
        return self.truncate(edge_magnitude)

    def name(self):
        return "Prewitt Filter"