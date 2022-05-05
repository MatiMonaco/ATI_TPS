import numpy as np
from filters.filter import Filter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import math


class HoughTransform(Filter):

    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback
        self.params = None
        self.params_len = None
        self.param_values = None
        self.border_detection_filter = None
        self.umbralization_filter = None
        self.epsilon = 1
        self.accumulator = None

        self.figure_qty = 80

    def setupUI(self):

        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)
        #self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)

        self.figure_qty_label = QtWidgets.QLabel(self.groupBox)
        self.figure_qty_label.setText("Figure %")
        self.figure_qty_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.figure_qty_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.figure_qty_label)

        self.figure_qty_slider = QtWidgets.QSlider(self.groupBox)
        self.figure_qty_slider.setMaximum(100)
        self.figure_qty_slider.setTracking(True)
        self.figure_qty_slider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalLayout.addWidget(self.figure_qty_slider)

        self.figure_qty_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.figure_qty_line_edit.editingFinished.connect(
            lambda: self.changeSlider(self.figure_qty_line_edit.text()))
        onlyInt = QIntValidator()
        onlyInt.setBottom(0)
        onlyInt.setTop(100)
        self.figure_qty_line_edit.setValidator(onlyInt)

        self.figure_qty_slider.valueChanged.connect(self.changeFigureQtyText)

        self.horizontalLayout.addWidget(self.figure_qty_line_edit)

        line = QtWidgets.QFrame(self.groupBox)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line)

        self.epsilon_label = QtWidgets.QLabel(self.groupBox)
        self.epsilon_label.setText(
            "<html><head/><body><span>&epsilon;</span></body></html>")
        self.epsilon_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.epsilon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.epsilon_label)

        self.epsilon_line_edit = QtWidgets.QLineEdit(self.groupBox)
        onlyDouble = QDoubleValidator()
        onlyDouble.setBottom(0)
        self.epsilon_line_edit.setValidator(onlyDouble)
        self.epsilon_line_edit.editingFinished.connect(self.changeEpsilon)
        self.horizontalLayout.addWidget(self.epsilon_line_edit)

        line2 = QtWidgets.QFrame(self.groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line2)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)

        self.figure_qty_slider.setValue(self.figure_qty)
        self.figure_qty_line_edit.setText(str(self.figure_qty))
        self.epsilon_line_edit.setText(str(self.epsilon))

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 1)
        self.horizontalLayout.setStretch(7, 1)

    def changeSlider(self, value):

        self.figure_qty = value
        self.figure_qty_slider.setValue(value)

    def changeFigureQtyText(self, value):

        self.figure_qty = value
        self.figure_qty_line_edit.setText(str(value))

    def changeEpsilon(self, value):
        self.epsilon = value

    def set_parameters(self):
        pass

    def apply(self, img_arr):
        # self.border_detection_filter.channels = self.channels
        # edges_image = self.border_detection_filter.apply(img_arr)
        # self.umbralization_filter.channels = self.channels
        # edges_image = self.umbralization_filter.apply(img_arr)

        # Creo matriz acumuladora
        if self.accumulator is None:
            # La matriz acumulador A tiene la misma dimension en la que se decide discretizar el espacio de par´ametros. La celda A(i, j) corresponde a las coordenadas del espacio de params (ai, bj)
            self.accumulator = self.calculate_accumulator()

        # Para cada elemento (ai, bj) y para cada pixel (xk , yk ) blanco, sumarle al accum
        # las posiciones de los pixels blancos
        edge_pixels = np.argwhere(img_arr == 255)
        edge_pixels[:, 0] -= math.floor(img_arr.shape[0]/2)
        edge_pixels[:, 1] -= math.floor(img_arr.shape[1]/2)

        for edge_pixel_coords in edge_pixels:
            self.accumulate(edge_pixel_coords[1], edge_pixel_coords[0])

        # Examinar el contenido de las celdas del acumulador con altas concentraciones
        accum_quantity = math.floor(
            np.prod(self.param_values_len)*self.figure_qty/100.0)  # TODO check
        figure_params_indexes = self.top_n_indexes(
            self.accumulator, accum_quantity)

        # Dibujar  figuras TODO

        final_img = self.draw_figure(img_arr, figure_params_indexes)
        print(f"final img = {final_img}")
        return final_img

    def top_n_indexes(self, arr, n):
        idx = np.argpartition(arr, arr.size-n, axis=None)[-n:]
        width = arr.shape[1]
        return [divmod(i, width) for i in idx]

    def accumulate(self, x, y):
        pass

    def draw_figure(self, img_arr, lines):
        pass

    def calculate_accumulator(self):

        self.param_values = list()
        param_values_len = list()

        for i in range(self.params_len):
            min = self.params[i]['min']
            max = self.params[i]['max']
            parts = self.params[i]['parts']
            param_values = list(np.linspace(min, max, parts))
            print(
                f"param {self.params[i]['param_name']} values: {param_values}")
            # TODO check que la matrix sea de partsxparts
            param_values_len.append(len(param_values))
            # estos son los posibles valores que puede tomar ese param
            self.param_values.append(param_values)

        accumulate = np.zeros(tuple(param_values_len))

        print("acummulate: ", accumulate.shape)

        return accumulate
