
from filters.spatial_domain.spatial_domain import SpatialDomainFilter
import numpy as np

class BorderMaskFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUi()
        
    def setupUi(self):
        super().setupUi()
    
    def name(self):
        return "Border Mask Filter"
        
    def generate_mask(self,mask_size): 
       
        center = int(mask_size/2)
        mask = np.zeros((mask_size, mask_size)) - 1
        mask[center,center] = mask_size ** 2 - 1
        return mask / (mask_size**2), mask_size