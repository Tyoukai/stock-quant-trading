import matplotlib.pyplot as plt
import numpy as np

# plt.contour是python中用于画等高线的函数
x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = X * 2 + Y * 2
C = plt.contour(x, y, Z, [2,5,8,10])
plt.clabel(C, inline=True, fontsize=10)
plt.show()
