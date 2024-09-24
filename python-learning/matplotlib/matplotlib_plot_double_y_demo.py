import matplotlib.pyplot as plt
import numpy as np

# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False
figure = plt.figure(1, (10, 8))

apple = [88, 80, 79, 81, 91, 95, 96]
banana = [70, 80, 81, 82, 75, 90, 89]
x = np.arange(1, 8)

ax1 = figure.add_subplot(111)
ax1.plot(x, apple, 'r--', label='苹果')
ax1.set_ylabel('苹果价格')
ax1.annotate('最低价', xy=(3, 79), xytext=(2, 78), arrowprops=dict(arrowstyle='->', connectionstyle='angle3,angleA=0,angleB=-90'))

ax2 = ax1.twinx()
ax2.plot(x, banana, 'k-', label='香蕉')
ax2.set_ylabel('香蕉价格')

figure.legend(loc=3, bbox_to_anchor=(0, 0), bbox_transform=ax1.transAxes)
plt.show()



