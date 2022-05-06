from re import X
import numpy as np
import math



def _get_index(index):
  
    new_index = list()
    for parts in [3,3,3][1:]:
     
        div = divmod(index,parts)
      
        new_index.append(div[1])
        index = div[0]
    new_index.append(div[0])
    return tuple(new_index[::-1])
def _top_n_indexes(arr, n):
        idx = np.argpartition(arr, arr.size-n, axis=None)[-n:]
        print(idx)
        print(idx[::-1])
    
        return [_get_index(i) for i in idx[::-1]]

arr = np.arange(0,27).reshape(3,3,3)

#np.random.shuffle(arr)
print(arr)
top_n =_top_n_indexes(arr,3)

print(top_n)




