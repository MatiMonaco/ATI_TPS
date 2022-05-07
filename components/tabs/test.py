import numpy as np

LIns = np.array([[0,0],[1,1],[2,2]])

arr = np.arange(0,27).reshape(3,3,3)

print(arr)


print("LINS X: ",LIns[:,0])
print("LINS Y: ",LIns[:,1])
arr[LIns[:,0],LIns[:,1]]= np.array([255,0,0])

print(arr)