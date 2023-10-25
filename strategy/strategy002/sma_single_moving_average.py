import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts

ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
pro = ts.pro_api()
df = pro.daily(ts_code='000001.SZ', start_date='20230818', end_date='20230928')
df = df.reindex(df.index[::-1])

calculate_df = df.loc[19:0, ['trade_date', 'close']]
avg_10 = []
avg_value = []
period = 10

for close in df['close']:
    avg_10.append(close)
    if len(avg_10) > period:
        del avg_10[0]
    if len(avg_10) == period:
        avg_value.append(np.mean(avg_10))
del avg_value[len(avg_value) - 1]
calculate_df['avg_10'] = avg_value
# calculate_df = calculate_df.assign(avg_10=pd.Series(avg_value, index=calculate_df.index))
print(calculate_df)

fig = plt.figure(1, (15, 10))
ax = fig.add_subplot(111)

ax.plot(calculate_df['trade_date'], calculate_df['close'], 'b-', 'close')
ax.plot(calculate_df['trade_date'], calculate_df['close'], 'r--', 'avg_10')

ax.set_ylim([8, 12])
ax.set_xticks(['20230901', '20230908', '20230915', '20230922', '20230928'])
ax.legend(loc=3)
plt.show()





