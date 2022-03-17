from filters.multiplicative_noise import MultiplicativeNoise
import numpy as np


class RayleighNoiseFilter(MultiplicativeNoise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.epsilon = 1
        self.setupUI()

    def setupUI():
        pass

    def generateNoise(self):
        return np.random.Generator.rayleigh(self.epsilon)
