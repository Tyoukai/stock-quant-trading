import tushare as ts

ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
pro = ts.pro_api()

df = pro.daily(ts_code='000001.SZ', start_date='20230901', end_date='20230930')
print(df)



