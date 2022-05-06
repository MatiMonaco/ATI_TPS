import numpy as np
print("TEST INIT")
a = np.zeros((2,2,2))
    
print(a)  
    
N = 5
idx = np.argsort(a.ravel())[-N:][::-1] #single slicing: `[:N-2:-1]`
topN_val = a.ravel()[idx]
row_col = np.c_[np.unravel_index(idx, a.shape)]

print(topN_val)