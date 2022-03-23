
from filters.spatial_domain.spatial_domain import SpatialDomainFilter
import numpy as np


class MeanMaskFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
     
        self.setupUi()

    def setupUi(self):
        super().setupUi()
        
    def generate_mask(self,mask_size): 
      
        return np.zeros((mask_size, mask_size))+1/mask_size**2, mask_size