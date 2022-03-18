
from filters.spatial_domain.spatial_domain import SpatialDomainFilter
import numpy as np

class GaussMask(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        

    def generate_mask(self,mask_size): 
        
        pass