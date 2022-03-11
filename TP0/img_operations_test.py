from PIL import Image, ImageChops
import numpy as np

def operate_lib(img1_path, img2_path, operation):
    im1 = Image.open(img1_path) 
    im1_arr = np.array(im1) 

    im2 = Image.open(img2_path)
    im2_arr = np.array(im2)

    #im3_arr = im1_arr + im2_arr
    #im3_arr = im3_arr - im3_arr.min() / (im3_arr.min()+im3_arr.max())
    #print(im3_arr.min(), np.uint8(im3_arr.max()))


    #im3 = Image.fromarray(np.uint8(im3_arr)) 
    if operation == 'multiply': 
        im3 = ImageChops.multiply(im1, im2)
    elif operation == 'substract':
        im3 = ImageChops.subtract(im1, im2)
    im3.save('new_img.png')

# applying multiply method
#im3 = ImageChops.add(im1, im2)
#im3 = ImageChops.multiply(im1, im2)
#im3 = ImageChops.subtract(im1, im2)
 