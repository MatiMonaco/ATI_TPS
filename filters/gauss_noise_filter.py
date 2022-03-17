from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QColor, QRgba64, QIntValidator

from filters.additive_noise import AdditiveNoise
from .filter import Filter
import qimage2ndarray
from time import process_time_ns
import numpy as np


class GaussNoise(AdditiveNoise):

    def __init__(self,update_callback):
        super().__init__(update_callback)
        self.setupUI()
        
    def setupUI():
         pass

    def generateNoise(mu, sigma):
        return np.random.default_rng().normal(mu, sigma)

