import numpy as np

arr = np.array([[[255,244,233],[255,244,233]],[[255,244,233],[255,244,233]]])
print(f"size:{arr.shape}\n{arr}")
print(arr[:,:,1].flatten())