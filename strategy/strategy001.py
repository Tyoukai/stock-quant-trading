import tushare as ts
import numpy as np
import matplotlib.pyplot as plt

ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
pro = ts.pro_api()
df = pro.daily(ts_code='000001.SZ', start_date='20230901', end_date='20230930')

df = df.reindex(df.index[::-1])
df['signal'] = np.where(df['change'] > 0, 1, 0)

fig = plt.figure(num=1, figsize=(10, 8))
ax = fig.add_subplot(111)
ax.plot(df['trade_date'], df['close'])

up_point = []
up_date = []
down_point = []
down_date = []
for index in df.index:
    if df['signal'][index]:
        up_point.append(df['close'][index])
        up_date.append(df['trade_date'][index])
    else:
        down_point.append(df['close'][index])
        down_date.append(df['trade_date'][index])

ax.scatter(up_date, up_point, c='r', marker='v')
ax.scatter(down_date, down_point, c='r', marker='^')

plt.show()



