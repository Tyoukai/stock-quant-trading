from backtest.BaseApi import *
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

stock = get_daily_stock_by_ak('000703', '20240219', '20240226')
# stock = get_daily_stock_by_ak('002028', '20240219', '20240223')
x = np.arange(len(stock.index)).reshape(-1, 1)
stock['mid_close'] = (stock['open'] + stock['close']) / 2.0
lr = LinearRegression().fit(x, stock['mid_close'])
print(lr.coef_)

figure = plt.figure(1, (10, 8))
ax = figure.add_subplot(111)
ax.plot(x, lr.predict(x))
plt.show()
