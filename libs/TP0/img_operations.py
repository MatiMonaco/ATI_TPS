from PIL import Image, ImageChops
import numpy as np
from PyQt5.QtGui import QPixmap, QColor

def normalize(x): 
    return x - x.min() / (x.min()+x.max())

def save(img_arr):

    img = Image.fromarray(np.uint8(img_arr)) 
    img.save('new_img.png')

def imgs_to_array(img1_path , img2_path ):
    
    img1 = Image.open(img1_path)   

    img2 = Image.open(img2_path) 

    img1_arr = np.array(img1)
    img2_arr = np.array(img2)

    return img1_arr, img2_arr

def operate(img1_path, img2_path, operation): 
     
    # Convert Images to Array 
    img1_arr,img2_arr = imgs_to_array(img1_path, img2_path)
    
    # Operate and apply linear transformation
    if operation == 'sum': #TODO hacer enums
            img3_arr = img1_arr + img2_arr 

    elif operation == 'substract': #TODO que pasa con los negativos? 
        img3_arr = img1_arr - img2_arr 
        img3_arr[ img3_arr < 0] = 0
        

    elif operation == 'multiply': 
        img3_arr = img1_arr * img2_arr  

    img3_arr =  normalize(img3_arr)

    save(img3_arr)

    return img3_arr
 