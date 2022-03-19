
from filters.spatial_domain.spatial_domain import SpatialDomainFilter
import numpy as np
import statistics

TOTAL_CHANNELS = 3

class WeightedMedianMask(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        

    def generate_mask(self,mask_size): 
        
        mask = [[1,2,1],[2,4,2],[1,2,1]]

        return np.array(mask), 3

    def apply_mask(self, sub_img, mask): 
                
        pixels_by_channel = []     
    
        for channel in range(0,TOTAL_CHANNELS):
            sub_img_by_channel = sub_img[:, :, channel]
            sub_img_arr = sub_img_by_channel.flatten()
            mask_arr = mask.flatten()
          
            for pixel, amount in zip(sub_img_by_channel, mask_arr): 
                for i in range(amount):
                    np.append(sub_img_arr, pixel)         

            median = statistics.median(sub_img_arr)         
            pixels_by_channel.append(median) 
    
        return pixels_by_channel
        