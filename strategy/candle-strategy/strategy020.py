from backtest.BaseApi import *
import numpy as np
import time


def hit_window_feature(code, start_date, end_date):
    try:
        stock = get_daily_stock_by_ak(code, start_date, end_date)
        if np.any(stock.isnull()):
            return False
        time.sleep(0.005)

        index = len(stock.index) - 1
        today_open = stock['open'].iloc[index]
        today_close = stock['close'].iloc[index]
        today_high = stock['high'].iloc[index]
        today_low = stock['low'].iloc[index]
        yesterday_open = stock['open'].iloc[index - 1]
        yesterday_close = stock['close'].iloc[index - 1]
        yesterday_high = stock['high'].iloc[index - 1]
        yesterday_low = stock['low'].iloc[index - 1]

        if today_open < today_close:
            return False

        #
        if today_low < yesterday_low and (today_high - yesterday_low) < 0:
            print(code)
            return True
        if today_high > yesterday_high and (today_low - yesterday_high) > 0:
            print(code)
            return True

        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['signal'] = stock_df.apply(lambda x: hit_window_feature(x['code'], '20240307', '20240314'), axis=1)
    stock_df = stock_df.dropna(axis=0, how='any').reset_index(drop=True)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
