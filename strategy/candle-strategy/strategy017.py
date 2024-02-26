from backtest.BaseApi import *
from backtest.StockShape import *
from sklearn.linear_model import LinearRegression
import time
import numpy as np


def hit_feature(code, start_date, end_date):
    try:
        stock = get_daily_stock_by_ak(code, start_date, end_date)
        if np.any(stock.isnull()):
            return False
        time.sleep(0.005)

        today_open = stock['open'].iloc[len(stock.index) - 1]
        today_close = stock['close'].iloc[len(stock.index) - 1]
        yesterday_high = stock['high'].iloc[len(stock.index) - 2]
        yesterday_low = stock['low'].iloc[len(stock.index) - 2]
        yesterday_open = stock['open'].iloc[len(stock.index) - 2]
        yesterday_close = stock['close'].iloc[len(stock.index) - 2]
        the_day_before_yesterday_open = stock['open'].iloc[len(stock.index) - 3]
        the_day_before_yesterday_close = stock['close'].iloc[len(stock.index) - 3]

        if the_day_before_yesterday_open <= the_day_before_yesterday_close:
            return False
        if today_close <= today_open:
            return False

        if yesterday_open <= yesterday_close and yesterday_close >= the_day_before_yesterday_close:
            return False
        if yesterday_open > yesterday_close and yesterday_open >= the_day_before_yesterday_close:
            return False

        if is_star(yesterday_open, yesterday_close, yesterday_high, yesterday_low):
            x = np.arange(len(stock.index)).reshape(-1, 1)
            stock['mid_close'] = (stock['open'] + stock['close']) / 2.0
            lr = LinearRegression().fit(x, stock['mid_close'])
            if lr.coef_ <= -0.2:
                print(code)
                return True
        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    """
    启明星形态判断
        找出看涨的反转趋势图
    """
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['star_signal'] = stock_df.apply(lambda x: hit_feature(x['code'], '20240219', '20240226'), axis=1)
    stock_df = stock_df[stock_df['star_signal']]
    print(stock_df)
