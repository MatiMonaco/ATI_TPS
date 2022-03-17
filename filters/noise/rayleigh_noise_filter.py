from filters.noise.multiplicative_noise import MultiplicativeNoise
import numpy as np


class RayleighNoiseFilter(MultiplicativeNoise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.epsilon = 1

    def setupUI(self):
        super().setupUI()

    def generateNoise(self, size):
        return np.random.default_rng().rayleigh(scale=self.epsilon, size=size)
