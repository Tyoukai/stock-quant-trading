import numpy as np
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt

ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
pro = ts.pro_api()
df = pro.daily(ts_code='000001.SZ', start_date='20230901', end_date='20230930')

df = df.reindex(df.index[::-1])
df['price'] = df['close']
df['diff'] = df['price'].diff()
df = df.fillna(0.0)

df['signal'] = np.where(df['diff'] >= 0, 0, 1)
df['order'] = df['signal'].diff() * 1700
df = df.fillna(0.0)

map = {
    'date': df['trade_date'],
    'price': df['price'],
    'diff': df['diff'],
    'signal': df['signal'],
    'order': df['order']
}

df = pd.DataFrame(map)
print(df)

init_cash = 20000.0

df['stock'] = df['price'] * df['order']
df['cash'] = init_cash - (df['order'].diff() * df['price']).cumsum()
df['total'] = df['stock'] + df['cash']

print('=============')
df.fillna(0.0)
print(df)

fig = plt.figure(1, (10, 8))
ax = fig.add_subplot(111)
ax.plot(df['date'], df['total'], 'r-', lable='total')
ax.plot(df['date'], df['order'].cumsum() * df['price'], 'b--', label='stock')

ax.set_ylim([0, 21001])

ax.set_xticks(['20230901', '20230908', '20230915', '20230922', '20230929'])
ax.set_yticks(np.linspace(0, 21000, 10))
ax.legend(loc=3)
plt.show()


