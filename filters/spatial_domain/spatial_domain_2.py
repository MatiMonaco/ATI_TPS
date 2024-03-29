
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

    def setupUI(self):

        self.spatial_domain_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.spatial_domain_groupBox)
        self.spatial_domain_groupBox.setTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.spatial_domain_groupBox)
        self.spatial_domain_horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.spatial_domain_horizontalLayout)
        self.size_label = QtWidgets.QLabel(self.spatial_domain_groupBox)
        self.size_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.size_label.setScaledContents(False)
        self.size_label.setAlignment(QtCore.Qt.AlignCenter)
      
        self.spatial_domain_horizontalLayout.addWidget(self.size_label)

        self.size_line_edit = QtWidgets.QLineEdit(
            self.spatial_domain_groupBox)
      
        self.spatial_domain_horizontalLayout.addWidget(self.size_line_edit)

        self.btn_apply = QtWidgets.QPushButton(self.spatial_domain_groupBox)
      
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.spatial_domain_horizontalLayout.addWidget(self.btn_apply)

        self.spatial_domain_horizontalLayout.setStretch(0, 1)
        self.spatial_domain_horizontalLayout.setStretch(1, 6)
        self.spatial_domain_horizontalLayout.setStretch(2, 1)

      

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

    def mask_filtering(self,extended_img, mask, padding_size, norm=False):
        '''
            Retorna una nueva imagen que resulta de aplicar la mascara a la
            imagen original

                Parametros:
                    extended_img (np.ndarray): Imagen original con padding
                    mask (np.ndarray): Mascara a aplicar
                    padding_size (int): Tamaño del padding

                Retorna:
                    new_img (np.ndarray): imagen que resulta de aplicar la mascara a la imagen original
        '''

        new_img = []
        for x in range(padding_size, extended_img.shape[0]-padding_size):
            new_img.append([])
            for y in range(padding_size, extended_img.shape[1]-padding_size):
               
                sub_img = extended_img[x-padding_size:x +
                                       padding_size+1, y-padding_size:y+padding_size+1]
                # print(f"sub_img: {sub_img.shape}")
                pixel = self.apply_mask(sub_img, mask)
                # print(f"pixel: {pixel.shape}")
                new_img[x-padding_size].append(pixel)
        if norm:
            return self.normalizeIfNeeded(np.array(new_img))
        return np.array(new_img)

    def apply_mask(self, sub_img, mask=None):
        '''
            Retorna el valor del pixel resultante de 
            la operacion de convolucion con la mascara
        '''
        return np.sum(np.multiply(sub_img, mask[:, :, np.newaxis]), axis=(1,0))

    
    def generate_mask(self, mask_size):
        '''
            Genera la la mascara y el tamaño de la mascara,
            como es cuadrada devuelve un unico valor. Si modifica 
            el tamaño de la mascara, lo devuelve modificado, si
            no lo modifica devuelve el mismo valor.
        '''
        return None, mask_size

    # complete borders repeating rows and columns
    def complete_image(self, img, mask_size):
        '''
            Completa la imagen con padding circular
        '''

        height = img.shape[0]
        width = img.shape[1]
        padding_size = int(np.floor(mask_size/2))
       
        new_img = np.zeros((height+2*padding_size, width+2*padding_size, self.channels))
        # ext_height = new_img.shape[0]
        # ext_width = new_img.shape[1]
        # n = padding_size
        new_img[padding_size:new_img.shape[0]-padding_size,padding_size:new_img.shape[1]-padding_size] = img
        # first n rows = old last n row
        # new_img[0:padding_size, 1:width+1] = img[height-padding_size:height]
        # # last n row  = old first n row
        # new_img[ext_height - padding_size: ext_height,
        #         1:width+1] = img[0:padding_size]

        # # left col  = old right col
        # new_img[padding_size:padding_size + height,
        #         0:padding_size] = img[:, width-padding_size:width]
        # # right col = old left col
        # new_img[padding_size:padding_size + height, ext_width -
        #         padding_size:ext_width] = img[:, 0:padding_size]

        # # complete middle
        # new_img[padding_size:ext_height - padding_size,
        #         padding_size:ext_width - padding_size] = img

        return new_img, padding_size

    def apply(self, img_arr):
        '''
            Retorna la imagen filtrada con una mascara. 
            1. Calcula la mascara
            2. Extiende la imagen con padding 
            3. Aplica y retorna la imagen filtrada
        ''' 
        mask, mask_size = self.generate_mask(self.mask_size)
     
    

        extended_img, padding_size = self.complete_image(img_arr, mask_size)

        return self.mask_filtering(extended_img, mask, padding_size)
