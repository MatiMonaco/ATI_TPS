from filters.noise.additive_noise import AdditiveNoise 
import numpy as np


class GaussNoiseFilter(AdditiveNoise):

    def __init__(self,update_callback):
        super().__init__(update_callback)
        self.mu = 50
        self.sigma = 0.5
        
    def setupUI(self):
        super().setupUI()

    def generateNoise(self):
        return np.random.default_rng().normal(self.mu, self.sigma)

