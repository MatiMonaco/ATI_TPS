from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt




class Tab(QtWidgets.QWidget):
  

    def __init__(self, name, *args, **kwargs):
        super(Tab, self).__init__(*args, **kwargs)
        self.setObjectName(name)
        self.setLayout(QtWidgets.QVBoxLayout())
