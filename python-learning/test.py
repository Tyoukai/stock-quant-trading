import numpy as np

first_array = np.array([2, 3, 4])
print(first_array)

print("==============")
print(np.zeros((2, 3)).ndim)
print("==============")
print(np.zeros((2, 3, 4)).ndim)
print("==============")
print(np.zeros((2, 3, 4, 5)).ndim)
