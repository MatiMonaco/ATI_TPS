from PyQt5.QtGui import QPixmap
from ..filter import Filter
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtGui import QPixmap, QColor, QRgba64, QDoubleValidator 
import qimage2ndarray

from locale import atof


class GammaPowerFilter(Filter):

    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback
        self.gamma = 1
        self.SLIDER_MAXIMUM_VALUE = 200 # multiplicado por 100 porque despues divido por 100 para tener doubles value
       
        self.setupUI()

    def name(self):
        return "Gamma Power Filter"
        
    def setupUI(self):

        self.groupBox = QtWidgets.QGroupBox()
        self.layout().addWidget(self.groupBox)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.gamma_label = QtWidgets.QLabel(self.groupBox)
        self.gamma_label.setText("Gamma")
        self.gamma_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.gamma_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gamma_label.setObjectName("gamma_label")
        self.horizontalLayout.addWidget(self.gamma_label)

        self.slider = QtWidgets.QSlider(self.groupBox)
        self.slider.setMaximum(self.SLIDER_MAXIMUM_VALUE)
        self.slider.setTracking(True)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")

        self.horizontalLayout.addWidget(self.slider)

        self.gamma_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.gamma_line_edit.setObjectName("gamma_line_edit")
        self.gamma_line_edit.returnPressed.connect(
            lambda: self.changeSlider(self.gamma_line_edit.text()))
        #self.gamma_line_edit.setValidator(QDoubleValidator(0, 2,2))

        self.slider.valueChanged.connect(self.changeGammaText)

        self.horizontalLayout.addWidget(self.gamma_line_edit)
        spacerItem1 = QtWidgets.QSpacerItem(
            69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.setObjectName("btn_apply")
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Update")
        self.horizontalLayout.addWidget(self.btn_apply)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.slider.setValue(self.gamma)

    def changeSlider(self, value):
        self.gamma = float(value)
        self.slider.setValue(self.gamma*100)

    def changeGammaText(self, value):
       
        fvalue = float(value)
        self.gamma = fvalue/100
        self.gamma_line_edit.setText(str(fvalue/100))

    def apply(self,img):
        c = (self.L-1)**(1-self.gamma)
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
        print(" gamma img arr size: ", img_arr.shape)
        res_arr = c*(img_arr[:,:,0:self.channels]**self.gamma)
        return res_arr
