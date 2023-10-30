import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts
import numpy as np

ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
pro = ts.pro_api()
df = pro.daily(ts_code='000001.SZ', start_date='20230818', end_date='20230928')
df = df.reindex(df.index[::-1])

calculate_df = df.loc[:, ['trade_date', 'close']]
calculate_df['avg_5'] = calculate_df['close'].rolling(5, closed='left').mean()
calculate_df['avg_10'] = calculate_df['close'].rolling(10, closed='left').mean()

calculate_df = calculate_df.loc[19:0]
calculate_df['single'] = np.where(calculate_df['avg_5'] > calculate_df['avg_10'], 1, 0)
calculate_df['order'] = calculate_df['single'].diff()
calculate_df.fillna(0.0)

print(calculate_df)

fig = plt.figure(1, (15, 10))
ax = fig.add_subplot(111)

ax.plot(calculate_df['trade_date'], calculate_df['close'], 'b-', label='close')
ax.plot(calculate_df['trade_date'], calculate_df['avg_5'], 'y--', label='avg_5')
ax.plot(calculate_df['trade_date'], calculate_df['avg_10'], 'r--', label='avg_10')

df_buy = pd.DataFrame({
    'date': [],
    'close': []
})
df_sale = pd.DataFrame({
    'date': [],
    'close': []
})

for index in calculate_df['order'].index:
    if calculate_df['order'].iloc[index] > 0:
        df_buy['date'].loc[df_buy['date'].index] = calculate_df['trade_date'].iloc[index]
        df_buy['close'].loc[df_buy['close'].index] = calculate_df['close'].iloc[index]
    elif calculate_df['order'].iloc[index] < 0:
        df_sale['date'].loc[df_sale['date'].index] = calculate_df['trade_date'].iloc[index]
        df_sale['close'].loc[df_sale['close'].index] = calculate_df['close'].iloc[index]
ax.scatter(df_buy['date'], df_buy['close'], s=200, color='r', marker='^')
ax.scatter(df_sale['date'], df_sale['close'], s=200, color='g', marker='v')

ax.legend(loc=3)
ax.set_xticks(['20230901', '20230908', '20230915', '20230922', '20230928'])

fig.show()




