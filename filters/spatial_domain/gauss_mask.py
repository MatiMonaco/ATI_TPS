
from filters.spatial_domain.spatial_domain import SpatialDomainFilter
import numpy as np
import math

class GaussMask(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.mu = 0
        self.sigma = 4
        
    #TODO: missing setupUI with sigma parameter 1 - 6
    def generate_mask(self,mask_size): 
        mask_size = int(2 * self.sigma)+ 1
        center = int(math.floor(mask_size/2))
        mask = []
        for i in range(mask_size):
            mask.append([])
            for j in range(mask_size):
                mask[i].append((i-center)**2 + (j-center)**2)
        return 1/(self.sigma * np.sqrt(2 * np.pi)) * np.exp( - (np.array(mask) - self.mu)**2 / (2 * self.sigma**2)), mask_size

    def setSigma(self, text):
        if text != '':
            self.sigma = float(text)