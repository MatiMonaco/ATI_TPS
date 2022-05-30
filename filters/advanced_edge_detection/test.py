from re import X
import numpy as np
import math

 
img = np.array([[[200,3,4],[100,255,255]],[[255,255,255],[100,100,100]]])
img2 = np.array([[[2,3,2],[100,255,255]],[[255,255,255],[100,100,100]]])
 
 
 

print(0.1*(img+img2)**2 - 0.1*(img+img2)*(img+img2))
 
 