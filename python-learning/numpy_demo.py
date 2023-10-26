import numpy as np

# 等差数列
print(np.linspace(50, 100, 6))

# 计算平均数
a_list = np.array([1, 2, 3])
print(np.mean(a_list))

metric = np.array([[1, 2], [3, 4]])
print(np.mean(metric))

# 计算每一列的平均值
print(np.mean(metric, axis=0))

# 计算每一行的平均值
print(np.mean(metric, axis=1))

print(np.flip(np.arange(0, 20, 1), 0))


