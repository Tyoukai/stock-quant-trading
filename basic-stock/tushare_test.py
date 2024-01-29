import tushare as ts
import matplotlib.pyplot as plt
import numpy as np

ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
pro = ts.pro_api()

df = ts.realtime_quote(ts_code='600000.SH', src='dc')
print(df)

# df = pro.daily(ts_code='000001.SZ', start_date='20230901', end_date='20230907')
# # print(df)
# 
# fig = plt.figure(1, (8, 6))
# ax = fig.add_subplot(111)
# 
# ax.set_ylim([7, 13])
# ax.set_yticks(np.linspace(7, 13, 14))
# 
# ax.plot(df['trade_date'], df['close'], 'r-^', label='close')
# ax.legend(loc=3, labelspacing=2, handlelength=3, fontsize=14, shadow=True)
# 
# plt.show()



