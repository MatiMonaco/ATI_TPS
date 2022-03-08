from PIL import Image, ImageChops
import numpy as np

im1 = Image.open(r"/home/eugenia/ati/a.png") 
im1_arr = np.array(im1) 

im2 = Image.open(r"/home/eugenia/ati/b.png")
im2_arr = np.array(im2)

im3_arr = im1_arr + im2_arr
im3_arr = im3_arr - im3_arr.min() / (im3_arr.min()+im3_arr.max())
print(im3_arr.min(), np.uint8(im3_arr.max()))


im3 = Image.fromarray(np.uint8(im3_arr)) 
im3.save('new_img.png')

# applying multiply method
#im3 = ImageChops.add(im1, im2)
#im3 = ImageChops.multiply(im1, im2)
#im3 = ImageChops.subtract(im1, im2)
 