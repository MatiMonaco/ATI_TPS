import qimage2ndarray
import math
import numpy as np
from filters.thresholding.thresholding_filter import ThresholdingFilter


class GlobalThresholdingFilter(ThresholdingFilter):

    def __init__(self):
        super().__init__()

    def get_threshold(self, channel_arr):

        # intial T (0;255) = img mean
        threshold = np.mean(channel_arr)
        delta_threshold = math.inf

        while delta_threshold > 1:                  # iterate until deltaT < 1
            white_pixels = []
            black_pixels = []

            for x in range(channel_arr.shape[1]):
                for y in range(channel_arr.shape[0]):

                    pixel = channel_arr[y, x]
                    if pixel < threshold:
                        # pixels that are going to be black, not yet.
                        black_pixels.append(pixel)
                    else:
                        # pixels that are going to be white
                        white_pixels.append(pixel)

            white_mean = np.mean(white_pixels)
            black_mean = np.mean(black_pixels)

            new_threshold = (white_mean+black_mean)/2

            delta_threshold = new_threshold - threshold
            threshold = new_threshold

        return threshold
