import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import numpy as np
import pandas as pd


fig = plt.figure()
ax = fig.add_subplot(111)
start_date = dt.datetime(2024, 8, 20)
end_date = dt.datetime(2024, 10, 23)
date_list = pd.date_range(start='20240820', periods=10, freq='1d').strftime('%Y-%m-%d').tolist()

x = []
for date_str in date_list:
    x.append(dt.datetime.strptime(date_str, '%Y-%m-%d'))

y = np.random.rand(len(x))
y1 = np.random.rand(len(x))
ax.plot_date(x, y,'g', label='222')
ax.plot_date(x, y1, '#000000')
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
daysLoc = mpl.dates.DayLocator()
# 设置次刻度间隔
ax.xaxis.set_minor_locator(daysLoc)
ax.legend(loc=3)
plt.show()
