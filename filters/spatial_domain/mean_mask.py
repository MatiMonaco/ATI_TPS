
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np


class MeanMaskFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
     
        self.setupUI()
    
    def name(self):
        return "Mean Mask Filter"
        
    def setupUI(self):
        super().setupUI()
        
    def generate_mask(self,mask_size): 
      
        return np.zeros((mask_size, mask_size))+1/mask_size**2, mask_size