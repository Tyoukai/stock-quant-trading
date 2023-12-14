import numpy as np

# # 等差数列
# print(np.linspace(50, 100, 6))
#
# # 计算平均数
# a_list = np.array([1, 2, 3])
# print(np.mean(a_list))
#
# metric = np.array([[1, 2], [3, 4]])
# print(np.mean(metric))
#
# # 计算每一列的平均值
# print(np.mean(metric, axis=0))
#
# # 计算每一行的平均值
# print(np.mean(metric, axis=1))
#
# print(np.flip(np.arange(0, 20, 1), 0))
#
# print(np.arange(1, 7, 1))

# # vstack 沿垂直方向拼接数组
# array1 = np.arange(10).reshape(2, 5)
# array2 = np.arange(10).reshape(2, 5)
# print(np.shape(array1))
# print(array1)
# print(array2)
# array3 = np.vstack([array1, array2])
# print(np.shape(array3))
# print(array3)
#
# # hstack 沿水平方向拼接数组
# array4 = np.hstack([array1, array2])
# print(np.shape(array4))
# print(array4)

# ravel 将多维数组展开为一维
# array1 = np.arange(6).reshape(2, 3)
# print(array1.ravel())
#
# array2 = np.arange(6).reshape(2, 3)
# print(np.vstack([array1, array2]).ravel())

# 标准差 np.std 默认除以n，加上ddof=1后除以n-1
# array = [0.1, -0.1091, -0.1429, 0.0952, 0.1739, 0.0185]
# print(np.std(array, ddof=1))

ones = np.ones(10) * 19
print(type(ones))
print(ones)

ones = np.ones((1, 10))
ones = np.ones((10, 1))
