import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
pro = ts.pro_api()
df = pro.daily(ts_code='000001.SZ', start_date='20230704', end_date='20230928')
df = df.reindex(df.index[::-1])

calculate_df = df.loc[:, ['trade_date', 'high', 'low', 'close']]
calculate_df['most_high'] = df['high'].rolling(20, closed='left').max()
calculate_df['most_low'] = df['low'].rolling(20, closed='left').min()
calculate_df = calculate_df.iloc[-20:]
calculate_df['buy'] = calculate_df['close'] > calculate_df['most_high']
calculate_df['sell'] = calculate_df['close'] < calculate_df['most_low']

print(calculate_df)

fig = plt.figure(1, (10, 8))
ax = fig.add_subplot(111)

ax.plot(calculate_df['trade_date'], calculate_df['most_high'], 'b--', label='up')
ax.plot(calculate_df['trade_date'], calculate_df['most_low'], 'g--', label='down')
ax.plot(calculate_df['trade_date'], calculate_df['close'], 'r-', label='close')

ax.set_xticks(['20230901', '20230908', '20230915', '20230922', '20230928'])
ax.legend(loc=3)
plt.show()





