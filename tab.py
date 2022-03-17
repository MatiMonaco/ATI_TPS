import numpy as np
arr = np.zeros((2,2,3))

arr[:,:,0] = 100


mask = np.random.randint(0,2,size=arr.shape).astype(np.bool)
print(mask)