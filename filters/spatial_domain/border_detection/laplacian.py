from filters.spatial_domain.border_detection.second_derivative import SecondDerivativeFilter

import numpy as np

class LaplacianFilter(SecondDerivativeFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.setupUI()
        
    def setupUI(self):
        super().setupUI()

    def generate_mask(self, mask_size):
        return np.array([
                        [0,  -1,  0],
                        [-1 , 4, -1],
                        [0 , -1, 0]]), mask_size 