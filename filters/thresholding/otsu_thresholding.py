import numpy as np
from filters.thresholding.thresholding_filter import ThresholdingFilter
import plotly.graph_objects as go
from PyQt5 import QtWidgets
class OtsuThresholdingFilter(ThresholdingFilter):


    def __init__(self):
        super().__init__()
        self.class_variances = None
        self.setupUI()

    
    def setupUI(self):
        super().setupUI()
        self.btn_show_histogram = QtWidgets.QPushButton(self.thresholding_groupBox)
     
        self.btn_show_histogram.clicked.connect(self.plot_variance)
        self.btn_show_histogram.setStyleSheet("font-weight: bold;color:white;")
        self.btn_show_histogram.setText("Show Class Variance")
        self.thresholding_horizontalLayout.addWidget(self.btn_show_histogram)


    def get_threshold(self, img_arr):
        
        w = img_arr.shape[1]
        h = img_arr.shape[0]
     
        relative_freqs = self.calculate_relative_freqs(img_arr,w,h)
        
        accum_freqs = self.calculate_accum_freqs(relative_freqs)
        

        accum_means = self.calculate_accum_means(relative_freqs)
        global_mean = accum_means[self.L-1]

        self.class_variances = self.calculate_class_variances(accum_means, global_mean, accum_freqs)
        
        for variance in self.class_variances.keys(): 
            thresholds = self.class_variances[variance]
            if len(thresholds) > 1:
                self.class_variances[variance] = [int(np.mean(thresholds))]

                

        # KEY: variance VALUE=t TODO
        
        max_ = max( self.class_variances.keys())
        max_t = sum( self.class_variances[max_]) / len( self.class_variances[max_])
        
        return max_t

    def calculate_relative_freqs(self,img_arr,w,h):
        graysRelativeFreqs = np.zeros(self.L)

        for i in range(h):
            for j in range(w):
                gray = img_arr[i,j]
                
                graysRelativeFreqs[gray] += 1
        totalPixels = w*h
        return graysRelativeFreqs / totalPixels

    def calculate_accum_freqs(self, graysRelativeFreqs):
        
        graysAccumulatedFreqs = np.zeros(self.L)
        graysAccumulatedFreqs[0] = graysRelativeFreqs[0]
      
        for gray in range(1,self.L):
            graysAccumulatedFreqs[gray] = graysAccumulatedFreqs[gray-1] + graysRelativeFreqs[gray]
        return graysAccumulatedFreqs

    def calculate_accum_means(self, relative_freqs): 
        accum_means = []
        for threshold in range(self.L): 
            mean = 0
            for i in range(threshold): 

                mean += i* relative_freqs[i]
            accum_means.append(mean)
                
        return accum_means

    def calculate_class_variances(self,accum_means, global_mean, accum_freqs):
        variances = {}
        for threshold in range(self.L): 
            accum_freq = accum_freqs[threshold]

            if accum_freq != 0 and (1-accum_freq) != 0: 
                variance = (global_mean * accum_freq  - accum_means[threshold])**2 / (accum_freq * (1-accum_freq))
                 
                if variances.get(variance) is None:
                    variances[variance] = []
                variances[variance].append(threshold)
            
        return variances

    def plot_variance(self): 
        if self.class_variances is None:
            print('Please apply filter first')
        fig = go.Figure()
        variances = list( self.class_variances.keys())
        thresholds =  np.array(list( self.class_variances.values())).flatten()
        print(variances)
        print(thresholds)
       
        #fig.add_trace(go.Histogram(x=img_arr))
        fig.add_trace(go.Scatter(x=thresholds, y=variances))

        fig.update_layout(
            title=f"Class Variances", 
            xaxis_title= "Threshold",
            yaxis_title="Class Variance",
                 font={'size': 18} 
        )    
        fig.show()  
        

    

   
    ###################################################################################################

    def name(self):
        return "Otsu Threshold"