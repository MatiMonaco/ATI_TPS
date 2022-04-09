import numpy as np
import qimage2ndarray
from filters.difussion.difussion import Difussion
from ..filter import Filter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator


class Isotropic(Difussion):

    def __init__(self, update_callback):
        super().__init__()

    
    def get_kernel(self, deriv, sigma):
        return 1