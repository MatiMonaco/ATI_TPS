from re import X
import numpy as np
import math


def _top_n_indexes(arr, n):
    idx = np.argpartition(arr, arr.size-n, axis=None)[-1:-(n+1):-1]
    return list(zip(*np.unravel_index(idx, arr.shape)))


arr = np.arange(0, 16).reshape(2, 4, 2)

print(arr)
top_n = _top_n_indexes(arr, 4)
print("top n: ", top_n)

print(arr[top_n])
