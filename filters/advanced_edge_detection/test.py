from re import X
import numpy as np
import math

 
img = np.array([[[255,100,255],[100,255,255]],[[255,255,255],[100,100,100]]])


 
img[img[:, :, :3] != 255] = 0

print(img)