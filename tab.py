import numpy as np


def generateRandomCoords(w, h, quantity):

    random_arr = np.random.default_rng().choice(
        w*h, size=quantity, replace=False)
    x = np.floor_divide(random_arr, w)
    y = random_arr - x*w
    return x, y


x, y = generateRandomCoords(2, 2, 2)
print(f"x: {x}")
print(f"y: {y}")

arr = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(arr)
print("vals:", arr[x, y])

values = np.array([-1, -2])[np.newaxis].T
print("values: ", values)

arr[x, y] *= values


print("despues: ", arr)

print(f"max: {np.max(arr)}")
print(f"min: {np.min(arr)}")
