import numpy as np
from filters.difussion.difussion import Difussion


class IsotropicFilter(Difussion):

    def __init__(self,update_callback):
        super().__init__(update_callback)
        self.setupUI()
        
    
    def setupUI(self):
        super().setupUI()

    def get_kernel(self, deriv, sigma):
        return 1

    def name(self):
        return "Isotropic Filter"