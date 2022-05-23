import enum
import re
import os
import io
from zipfile import ZipFile
from enum import Enum

from PIL import Image, ImageQt
import numpy as np
import qimage2ndarray

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
from dialogs.raw_size_input_dialog import RawSizeInputDialog

class OperationsEnum(Enum):
    SUMA = 0,
    RESTA = 1,
    MULTIPLICACION = 2,

def read_raw_image( imagePath):
    with open(imagePath, 'r') as infile:
        data = np.fromfile(infile, dtype=np.uint8)

        size = len(data)
        dialog = RawSizeInputDialog()

        width = 0
        height = 0
        code = 1
        while size != width * height and code == 1:
            code = dialog.exec()

            width, height = dialog.getInputs()

        if code == 0:
            return None

        data = data.reshape(height, width)

        return QPixmap.fromImage(qimage2ndarray.gray2qimage(data))

def image_to_byte_array(image: Image) -> bytes:
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def saveImages(parent, pixmaps):
    if len(pixmaps) == 1:
        saveImage(parent, pixmap=pixmaps[0])
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getSaveFileName(parent, "Save Images", "", ".zip", "")
    with ZipFile(f"{fileName}.zip", mode="w") as archive:
        for i, pixmap in enumerate(pixmaps):
            image = ImageQt.fromqpixmap(pixmap)
            archive.writestr(f"IMG{i}.{image.format.lower()}", image_to_byte_array(image))

def saveImage(parent,pixmap):
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getSaveFileName(parent, "Save Image", "", "Images (*.png *.xpm *.jpg *.nef)", "")

    file = open(fileName, 'w')
    image = ImageQt.fromqpixmap(pixmap)
    print(f'LOG: saved filtered image to {file.name}')
    image.save(file.name)

IMG_NAME_PATT = "[a-zA-Z]*([0-9]+)\.(png|jpg|jpeg|ppm|pgm|raw)"

def openImageOrZip():
    '''
        Retorna un array de pixmaps de imagenes.
        - Si es un ZIP, extrae las imagenes y retorna las imagenes
        en order segun el nombre img{number}.ext
        - Si es una imagen sola retorna la imagen
    '''
    path, _ = QFileDialog.getOpenFileName()
    if path is None or path == "":
        return
    split_path = os.path.splitext(path)
    file_extension = split_path[1]
    if file_extension.lower() == ".zip":
        imgs = []
        with ZipFile(path, mode='r') as zip:
            for img in zip.namelist():
                res = re.match(
                    IMG_NAME_PATT, img, re.IGNORECASE)
                if res:
                    num = int(res.group(1))
                    pixmap = QPixmap()
                    pixmap.loadFromData(zip.read(img))
                    imgs.append((num, pixmap))
        imgs = sorted(imgs, key=lambda img: img[0])
        return list(map(lambda img: img[1], imgs))
    else:
        return [imageToPixmap(path)]

def imageToPixmap(imagePath: str):
    split_path = os.path.splitext(imagePath)
    file_extension = split_path[1]

    pixmap = None
    if file_extension.upper() == ".RAW":

        pixmap = read_raw_image(imagePath)

    else:
        pixmap = QPixmap()
        pixmap.loadFromData(open(imagePath, "rb").read())
    return pixmap

def openImage():
    imagePath, _ = QFileDialog.getOpenFileName()

    if imagePath == None or imagePath == "":
        return None
        # this will return a tuple of root and extension
    return imageToPixmap(imagePath=imagePath)

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
    print("IMG 1: ")
    print(img1_arr)
    print("\n\nIMG 2: ")
    print(img2_arr)
    # Operate and apply linear transformation
    if operation == OperationsEnum.SUMA:
            result = img1_arr + img2_arr 

    elif operation == OperationsEnum.RESTA:  # TODO que pasa con los negativos?
        result = img1_arr - img2_arr
        result[result < 0] = 0
        print("\n\nRESULT: ")
        print(result)
        
    elif operation == OperationsEnum.MULTIPLICACION:
        result = img1_arr * img2_arr

    result = normalize(result)

    return qimage2ndarray.array2qimage(result)
 