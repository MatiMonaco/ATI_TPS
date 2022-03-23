from PIL import Image
import numpy as np
from PyQt5.QtGui import QPixmap, QColor
import qimage2ndarray
from enum import Enum


class OperationsEnum(Enum):
    SUMA = 0,
    RESTA = 1,
    MULTIPLICACION = 2,
 

def normalize(x): 
    return x - x.min() / (x.min()+x.max())

def save(img_arr):

    img = Image.fromarray(np.uint8(img_arr)) 
    img.save('new_img.png')

def imgs_to_array(img1 , img2 ):
    
    img1_arr = qimage2ndarray.rgb_view(img1)
    img2_arr = qimage2ndarray.rgb_view(img2)

    return img1_arr, img2_arr

def operate(img1, img2, operation): 
     
    # Convert Images to Array 
    img1_arr, img2_arr = imgs_to_array(img1, img2)
    result  = None
    # Operate and apply linear transformation
    if operation == OperationsEnum.SUMA:
            result = img1_arr + img2_arr 

    elif operation == OperationsEnum.RESTA:  # TODO que pasa con los negativos?
        result = img1_arr - img2_arr
        result[result < 0] = 0
        
    elif operation == OperationsEnum.MULTIPLICACION:
        result = img1_arr * img2_arr

    result = normalize(result)

    return qimage2ndarray.array2qimage(result)
 