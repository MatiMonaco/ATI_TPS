from PyQt5 import  QtWidgets
from ..filter import Filter
import qimage2ndarray
import numpy as np
from time import process_time_ns
from PyQt5.QtGui import QPixmap
import math
class EqualizationFilter(Filter):

    def __init__(self):
        super().__init__()

        
    def calculateGraysRelativeFreqs(self,img_arr,w,h):
        graysRelativeFreqs = np.zeros((3, self.L))

        for channel in range(0,3):
            for i in range(h):
                for j in range(w):
                    gray = img_arr[i,j,channel]
                   
                    graysRelativeFreqs[channel,gray] += 1
        totalPixels = w*h
        return graysRelativeFreqs / totalPixels

    def calcualteGraysAccumulatedFreqs(self, graysRelativeFreqs):
        graysAccumulatedFreqs = np.zeros((3, self.L))
        graysAccumulatedFreqs[:, 0] = graysRelativeFreqs[:,0]
      
        for channel in range(0, 3):
            for gray in range(1,self.L):
                graysAccumulatedFreqs[channel,gray] = graysAccumulatedFreqs[channel, gray-1] + graysRelativeFreqs[channel, gray]
        return graysAccumulatedFreqs

    def apply(self, img):
        print(f"w: {img.width()}, h: {img.height()}")
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
        w = img_arr.shape[1]
        h = img_arr.shape[0]
        print(f"2 w: {w}, h: {h}")
        graysRelativeFreqs = self.calculateGraysRelativeFreqs(img_arr,w,h)
        #print("relative freqs: ", graysRelativeFreqs)
        #print("sum relative freqs: ", np.sum(graysRelativeFreqs))
        #print("relativefreqs[:,0]: ", graysRelativeFreqs[:, 0])
        graysAccumulatedFreqs = self.calcualteGraysAccumulatedFreqs(graysRelativeFreqs)
        #print("accumulated freqs: ",graysAccumulatedFreqs)
    
        t1_start = process_time_ns()
        for channel in range(0, 3):
            sMin = np.min(graysAccumulatedFreqs[channel,:])
        
            print("smin: ",sMin)
            for i in range(h):
                for j in range(w):
                    gray = img_arr[i, j, channel]
                  
                    img_arr[i, j, channel] = 255 * (graysAccumulatedFreqs[channel, gray]-sMin)/(1-sMin)
          
        print(img_arr)
        t1_stop = process_time_ns()
        print(f"Elapsed time: {t1_stop- t1_start}")
        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

