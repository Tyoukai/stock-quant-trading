import pandas as pd
import numpy as np

df = pd.DataFrame(np.arange(1, 8, 1), columns=['股价'])
df['行情变化信号'] = [0, 1, 1, 0, 0, 1, 0]
df['操作信号'] = df['行情变化信号'].diff()
df = df.fillna(0)
df['手持股票数量'] = df['操作信号'].cumsum() * 100
df['股票总价值'] = df['手持股票数量'].multiply(df['股价'], axis=0)
yesterday_cash = 20000.0
df['手上的现金'] = np.zeros((1, 7))[0]
df['当前操作的总价格'] = df['操作信号'].multiply(100, axis=0).multiply(df['股价'], axis=0)
for index in df.index:
    df.loc[index, '手上的现金'] = yesterday_cash - df.loc[index, '当前操作的总价格']
    yesterday_cash = df.loc[index, '手上的现金']
df['总价值'] = df['手上的现金'].add(df['股票总价值'], axis=0)
print(df)






