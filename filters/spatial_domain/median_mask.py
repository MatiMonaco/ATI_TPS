
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import statistics

TOTAL_CHANNELS = 3


class MedianMaskFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUI()
        
    def name(self):
        return "Median Mask Filter"
        
    def setupUI(self):
        super().setupUI()

    def apply_mask(self, sub_img, mask): 
   
        pixels_by_channel = []     
        
        for channel in range(0,self.channels):
            median = statistics.median(sub_img[:, :, channel].flatten())         
            pixels_by_channel.append(median) 
        
        return pixels_by_channel
            
    
    