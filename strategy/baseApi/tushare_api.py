import tushare as ts


def get_daily_stock(code, start_date, end_date):
    ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
    pro = ts.pro_api()
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    return df
