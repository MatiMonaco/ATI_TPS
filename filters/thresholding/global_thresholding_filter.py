import qimage2ndarray
import math
import numpy as np
from filters.thresholding.thresholding_filter import ThresholdingFilter

class GlobalThresholdingFilter(ThresholdingFilter):


    def __init__(self):
        super().__init__()
  
        
    def get_threshold(self, channel_arr):

        threshold = np.mean(channel_arr)            # intial T (0;255) = img mean  
        delta_threshold = math.inf

        while delta_threshold > 1:              # iterate until deltaT < 1
            white_pixels = []
            black_pixels = []
            print("Threshold: ",threshold)
            for x in range(channel_arr.shape[1]):
                for y in range(channel_arr.shape[0]):
          
                    pixel = channel_arr[x,y]
                    if pixel < threshold:         
                        black_pixels.append(pixel)  # pixels that are going to be black, not yet.
                    else:  
                        white_pixels.append(pixel)  # pixels that are going to be white

            white_mean = np.mean(white_pixels)
            black_mean = np.mean(black_pixels)

            new_threshold = (white_mean+black_mean)/2    

            delta_threshold = new_threshold - threshold
            threshold = new_threshold
        
        return threshold
     

  