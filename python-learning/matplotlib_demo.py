import matplotlib.pyplot as plt
import numpy as np

apple = [78, 80, 79, 81, 91, 95, 96]
banana = [70, 80, 81, 82, 75, 90, 89]
x = np.arange(1, 8)
fig = plt.figure(num=1, figsize=(6, 4))

ax = fig.add_subplot(111)
ax.plot(x, apple, 'r-.d', label='apple')
ax.plot(x, banana, 'c-d', label='banana')

# 设置x，y轴范围
ax.set_xlim([1, 7.1])
ax.set_ylim([40, 100])

# 设置x，y轴的刻度
ax.set_xticks(np.linspace(1, 7, 7))
ax.set_yticks(np.linspace(50, 100, 6))

# 设置x，y轴的标签
# rotation 设置标签倾斜角度
# fontproperties 设置字体
ax.set_xticklabels(["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"], fontproperties="SimHei", fontsize=12, rotation=10)
ax.set_yticklabels(["50kg", "60kg", "70kg", "80kg", "90kg", "100kg"])

# 设置图例
# loc:可取"best",1或者"upper right",2或"upper left",3或"lower left",4或"lower right",代表放不同位置
ax.legend(loc=3, labelspacing=2, handlelength=3, fontsize=14, shadow=True)

plt.show()
