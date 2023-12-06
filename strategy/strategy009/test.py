from backtest.BaseApi import *

df = get_daily_stock('510500.SZ', '20230818', '20230928')
print(df)

df = get_etf_inside('510500', '20230818', '20230928')
print(df)

