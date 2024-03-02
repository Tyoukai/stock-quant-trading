from backtest.BaseApi import *


def hit_feature(code, start_date, end_date):
    try:
        stock = get_daily_stock_by_ak(code, start_date, end_date)

    except Exception as e:
        return False


if __name__ == '__main__':
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['signal'] = stock_df.apply(lambda x: hit_feature(x['code'], 20240221, 20240301), axis=1)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
