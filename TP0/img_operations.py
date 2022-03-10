from PIL import Image, ImageChops
import numpy as np
 
def normalize(x): 
    return x - x.min() / (x.min()+x.max())

def save(img_arr):

    img = Image.fromarray(np.uint8(img_arr)) 
    img.save('new_img.png')

def imgs_to_array(img1 , img2 ):
    
    #TODO aca habria que pasar de ImageQT to array
    img1_arr = np.array(img1)
    img2_arr = np.array(img2)

    return img1_arr, img2_arr

def operate(img1, img2, operation): 
     
    # Convert Images to Array 
    img1_arr,img2_arr = imgs_to_array(img1, img2)
    
    # Operate and apply linear transformation
    if operation == 'sum': #TODO hacer enums
            img3_arr = img1_arr + img2_arr 

    elif operation == 'substract': #TODO que pasa con los negativos? 
        img3_arr = img1_arr - img2_arr 

    elif operation == 'multiply': 
        img3_arr = img1_arr * img2_arr 

    img3_arr =  normalize(img3_arr)

    save(img3_arr)

    return img3_arr
 