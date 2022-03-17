from filters.multiplicative_noise import MultiplicativeNoise
import numpy as np


class ExponentialNoiseFilter(MultiplicativeNoise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.lambda_ = 1
        self.setupUI()

    def setupUI():
        pass

    def generateNoise(self):
       return np.random.Generator.exponential(1/self.lambda_)
