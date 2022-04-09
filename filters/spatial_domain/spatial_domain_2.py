
import numpy as np
import qimage2ndarray
from ..filter import Filter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator


class SpatialDomainFilter(Filter):

    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback
        self.mask_size = 3

    def setupUi(self):

        self.spatial_domain_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.spatial_domain_groupBox)
        self.spatial_domain_groupBox.setTitle("")
        self.spatial_domain_groupBox.setObjectName("spatial_domain_groupBox")
        self.spatial_domain_horizontalLayout = QtWidgets.QHBoxLayout(
            self.spatial_domain_groupBox)
        self.spatial_domain_horizontalLayout.setObjectName(
            "spatial_domain_horizontalLayout")

        self.size_label = QtWidgets.QLabel(self.spatial_domain_groupBox)
        self.size_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.size_label.setScaledContents(False)
        self.size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.size_label.setObjectName("Matrix size")
        self.spatial_domain_horizontalLayout.addWidget(self.size_label)

        self.size_line_edit = QtWidgets.QLineEdit(
            self.spatial_domain_groupBox)
        self.size_line_edit.setObjectName("size_line_edit")
        self.spatial_domain_horizontalLayout.addWidget(self.size_line_edit)

        self.btn_apply = QtWidgets.QPushButton(self.spatial_domain_groupBox)
        self.btn_apply.setObjectName("btn_apply")
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.spatial_domain_horizontalLayout.addWidget(self.btn_apply)

        self.spatial_domain_horizontalLayout.setStretch(0, 1)
        self.spatial_domain_horizontalLayout.setStretch(1, 3)
        self.spatial_domain_horizontalLayout.setStretch(2, 1)

        self.spatial_domain_horizontalLayout.setStretch(5, 1)

        self.size_label.setText("Mask size")

        self.onlyInt = QIntValidator()
        self.onlyInt.setBottom(0)
        self.size_line_edit.setValidator(self.onlyInt)
        self.size_line_edit.editingFinished.connect(
            lambda: self.setMatrixSize(self.size_line_edit.text()))
        self.size_line_edit.setText(str(self.mask_size))

    def setMatrixSize(self, text):
         if text != '':
              newSize = int(text)
              if newSize % 2 == 0:
                  self.size_line_edit.setText(str(self.mask_size))
              else:
                    self.mask_size = int(text)
                    self.maskSizeChanged()

    def maskSizeChanged(self):
        pass

    def mask_filtering(self,extended_img,mask, padding_size, norm=True):


        new_img = []
        for x in range(padding_size, extended_img.shape[0]-padding_size):
            new_img.append([])
            for y in range(padding_size, extended_img.shape[1]-padding_size):
               
                sub_img = extended_img[x-padding_size:x +
                                       padding_size+1, y-padding_size:y+padding_size+1]
                pixel = self.apply_mask(sub_img, mask)
                new_img[x-padding_size].append(pixel)
        if norm:
            return self.normalizeIfNeeded(np.array(new_img))
        return np.array(new_img)

    def apply_mask(self, sub_img, mask=None):
        # print(f"sub img before: {sub_img}")
        # print(f"--------------------------------------")
        # print(f"mask: {mask}")
        pixels_by_channel = []
        for channel in range(0, self.channels):
            pixels_by_channel.append(
                np.sum(np.multiply(sub_img[:, :, channel], mask)))

        # print(f"sub img after: {np.array(pixels_by_channel)}")
        return np.array(pixels_by_channel)

    
    def generate_mask(self, mask_size):
        return None, mask_size

        #return self.get_mean_mask(mask_size)

    # complete borders repeating rows and columns
    def complete_image(self, img, mask_size):

        height = img.shape[0]
        width = img.shape[1]
        padding_size = int(np.floor(mask_size/2))

        new_img = np.zeros((height+2*padding_size, width+2*padding_size, 3))
        ext_height = new_img.shape[0]
        ext_width = new_img.shape[1]
        # n = padding_size
        # first n rows = old last n row
        new_img[0:padding_size, 1:width+1] = img[height-padding_size:height]
        # last n row  = old first n row
        new_img[ext_height - padding_size: ext_height,
                1:width+1] = img[0:padding_size]

        # left col  = old right col
        new_img[padding_size:padding_size + height,
                0:padding_size] = img[:, width-padding_size:width]
        # right col = old left col
        new_img[padding_size:padding_size + height, ext_width -
                padding_size:ext_width] = img[:, 0:padding_size]

        # complete middle
        new_img[padding_size:ext_height - padding_size,
                padding_size:ext_width - padding_size] = img

        return new_img, padding_size

    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')

        mask, mask_size = self.generate_mask(self.mask_size)

        extended_img, padding_size = self.complete_image(img_arr, mask_size)

        return self.mask_filtering(extended_img, mask, padding_size)
