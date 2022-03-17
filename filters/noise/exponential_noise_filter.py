from filters.noise.multiplicative_noise import MultiplicativeNoise
import numpy as np


class ExponentialNoiseFilter(MultiplicativeNoise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.lambda_ = 1
      
    def setupUI(self):
        super().setupUI()

    def generateNoise(self):
       return np.random.Generator.exponential(self.lambda_)
