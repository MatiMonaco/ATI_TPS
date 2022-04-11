from ..filter import Filter
import qimage2ndarray
import numpy as np
from PyQt5.QtGui import QPixmap


class EqualizationFilter(Filter):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Equalization Filter"

    def calculateGraysRelativeFreqs(self, img_arr, w, h):
        graysRelativeFreqs = np.zeros((3, self.L))

        for channel in range(0, self.channels):
            for i in range(h):
                for j in range(w):
                    gray = img_arr[i, j, channel]

                    graysRelativeFreqs[channel, gray] += 1
        totalPixels = w*h
        return graysRelativeFreqs / totalPixels

    def calculateGraysAccumulatedFreqs(self, graysRelativeFreqs):
        graysAccumulatedFreqs = np.zeros((3, self.L))
        graysAccumulatedFreqs[:, 0] = graysRelativeFreqs[:, 0]

        for channel in range(0, self.channels):
            for gray in range(1, self.L):
                graysAccumulatedFreqs[channel, gray] = graysAccumulatedFreqs[channel,
                                                                             gray-1] + graysRelativeFreqs[channel, gray]
        return graysAccumulatedFreqs

    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')[
            :, :, 0:self.channels]
        w = img_arr.shape[1]
        h = img_arr.shape[0]

        graysRelativeFreqs = self.calculateGraysRelativeFreqs(img_arr, w, h)
        graysAccumulatedFreqs = self.calculateGraysAccumulatedFreqs(
            graysRelativeFreqs)
        for channel in range(0, self.channels):
            sMin = np.min(graysAccumulatedFreqs[channel, :])

            for i in range(h):
                for j in range(w):
                    gray = img_arr[i, j, channel]

                    img_arr[i, j, channel] = 255 * \
                        (graysAccumulatedFreqs[channel, gray]-sMin)/(1-sMin)

        return img_arr
