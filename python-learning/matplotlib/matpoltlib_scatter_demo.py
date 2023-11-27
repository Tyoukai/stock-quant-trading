import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig = plt.figure(1, (10, 6))
ax = fig.add_subplot(111)

x = ['20230901', '20230902', '20230903', '20230904', '20230905']
y = np.linspace(0, 4, 5)

df = pd.DataFrame({
    'x': x,
    'y': y
})
ax.scatter(df.loc[y > 2].index, df['y'][y > 2], s=200, color='g', marker='^')


# s:点的大小 color:颜色
# ax.scatter(x, y, s=200, color='g', marker='^')

# 显示网格， linestyle：线的格式
plt.grid(color='r', linestyle='--')
fig.show()

