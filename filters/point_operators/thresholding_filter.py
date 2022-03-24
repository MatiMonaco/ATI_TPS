from ..filter import Filter
from .RGB_thresholding_filter import RGBThresholdingFilter
from .gray_thresholding_filter import GrayThresholdingFilter
from time import process_time_ns
import numpy as np

class ThresholdingFilter(Filter):

    def __init__(self,update_callback):
        super().__init__()
        self.rgb_filter = RGBThresholdingFilter(update_callback)
        self.gray_filter = GrayThresholdingFilter(update_callback)
        self.current_filter = self.rgb_filter
        

      

    def before(self,isGrayScale):
        print("isgrayscale: ",isGrayScale)
        if isGrayScale:
            self.current_filter = self.gray_filter
        else:
            self.current_filter = self.rgb_filter

    def apply(self,img):
       self.current_filter.apply(img)

   