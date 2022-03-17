import numpy as np
import math
import qimage2ndarray


def generateRandomCoords(w, h, quantity):

    random_arr = np.random.default_rng().choice(
        w*h, size=quantity, replace=False)
    x = np.floor_divide(random_arr, w)
    y = random_arr - x*w
    return x, y


def generateNoise(size):
    return np.random.default_rng().normal(50, scale=20, size=size)


img_arr = np.array(
    [[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]]).astype('float64')
print(f"img_arr:  {img_arr}")
width = img_arr.shape[0]
height = img_arr.shape[1]
print(f"w: {width}, h: {height}")
total_pixels = width*height
density = 0.5
pixel_proportion = math.floor(total_pixels * density)
print(f"proportion : {pixel_proportion}")

x, y = generateRandomCoords(width, height, pixel_proportion)
print(f"x: {x}, y: {y}")

noises = generateNoise(pixel_proportion)[np.newaxis].T
print(f"noises: {noises}")
print(f"pixels: {img_arr[x,y]}")
img_arr[x, y] += noises

print(f"after: {img_arr}")
max = np.max(img_arr)
min = np.min(img_arr)
print(f"min: {min}, max: {max}")
interval = max-min

img_arr[x, y] = 255*(img_arr[x, y] - min) / interval

print(f"after limit: {img_arr}")

img = qimage2ndarray.array2qimage(img_arr)
nuevo_img_arr = qimage2ndarray.rgb_view(img)
print(f"nuevo img arr: {nuevo_img_arr}")
