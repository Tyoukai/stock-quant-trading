import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(1, (15, 8))
ax = fig.add_subplot(111)

x = np.arange(10)
y = np.linspace(10, 40, 10)
# s:点的大小 color:颜色
ax.scatter(x, y, s=1500, color='g', marker='^')

fig.show()

