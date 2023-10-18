import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = [[78, 80, 79, 81, 91, 95, 96], [70, 80, 81, 82, 75, 90, 89]]
df = pd.DataFrame(data)

fig = plt.figure(1, (6, 4))
ax = fig.add_subplot(111)

x = np.arange(1, 8)
ax.plot(x, df.loc[0], 'r-.d', label='apple')
ax.plot(x, df.loc[1], 'c-d', label='banana')
ax.set_xlim([1, 7.1])
ax.set_ylim([40, 100])

ax.set_xticklabels(["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"], fontproperties="SimHei", fontsize=12, rotation=10)
ax.set_yticklabels(["50kg", "60kg", "70kg", "80kg", "90kg", "100kg"])

plt.show()