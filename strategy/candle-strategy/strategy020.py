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
        the_day_before_yesterday_open = stock['open'].iloc[index - 2]
        the_day_before_yesterday_close = stock['close'].iloc[index - 2]

        # 近三天必须都是上涨
        if today_open > today_close or yesterday_open > yesterday_close or the_day_before_yesterday_open > the_day_before_yesterday_close:
            return False
        # 近三天收盘价必须一天比一天高
        if today_close > yesterday_close > the_day_before_yesterday_close:
            # 今天与昨天之间形成窗口
            return today_low > yesterday_high

        return False
        # if today_open < today_close:
        #     return False
        #
        # if today_low < yesterday_low and (today_high - yesterday_low) < 0:
        #     print(code)
        #     return True
        # if today_high > yesterday_high and (today_low - yesterday_high) > 0:
        #     print(code)
        #     return True
        #
        # return False
    except Exception as e:
        return False


if __name__ == '__main__':
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['signal'] = stock_df.apply(lambda x: hit_window_feature(x['code'], '20240311', '20240318'), axis=1)
    stock_df = stock_df.dropna(axis=0, how='any').reset_index(drop=True)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
