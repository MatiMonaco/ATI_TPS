from PyQt5.QtGui import QPixmap
from ..filter import Filter
from PyQt5 import QtCore, QtWidgets
import qimage2ndarray

class NegativeFilter(Filter):

    def __init__(self):
        super().__init__()
      
       
    
        #self.setupUI()
     
    def name(self):
        return "Negative Filter"
           
    def setupUI(self):
        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")

     
        spacerItem1 = QtWidgets.QSpacerItem(
            69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.setObjectName("btn_apply")
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)

        self.horizontalLayout.setStretch(0, 9)
        self.horizontalLayout.setStretch(1, 1)
        

    # Get negative image: T(r) = -r + L-1
    def apply(self,img_arr):
      
        res_arr = -img_arr +self.L -1   
      
        return res_arr


