from backtest.BaseApi import *
from sklearn.linear_model import LinearRegression
import numpy as np
import time


def hit_feature(code, start_date, end_date):
    try:
        stock = get_daily_stock_by_ak(code, start_date, end_date)
        time.sleep(0.005)
        if np.any(stock.isnull()):
            return False

        today_open = stock['open'].iloc[len(stock.index) - 1]
        today_close = stock['close'].iloc[len(stock.index) - 1]
        yesterday_open = stock['open'].iloc[len(stock.index) - 2]
        yesterday_close = stock['close'].iloc[len(stock.index) - 2]
        yesterday_low = stock['low'].iloc[len(stock.index) - 2]
        yesterday_middle = (yesterday_open + yesterday_close) / 2.0

        if yesterday_open <= yesterday_close:
            return False
        if today_open >= today_close or today_open >= yesterday_low:
            return False
        if today_close < yesterday_middle:
            return False

        x = np.arange(len(stock.index)).reshape(-1, 1)
        stock['avg_price'] = (stock['close'] + stock['open']) / 2.0
        lr = LinearRegression().fit(x, stock['avg_price'])
        # 上涨趋势或过于平缓的直接返回false
        if lr.coef_ >= -0.2:
            return False

        print(code)
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    """
    获取沪深两市每日的斩回线形态
    """
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['signal'] = stock_df.apply(lambda x: hit_feature(x['code'], 20240202, 20240219), axis=1)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
