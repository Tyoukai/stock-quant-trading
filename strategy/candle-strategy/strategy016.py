from backtest.BaseApi import *
from backtest.StockShape import *
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

        # 昨天是涨的pass
        if yesterday_open <= yesterday_close:
            return False
        # 今天是跌的pass
        if today_open >= today_close:
            return False
        # 今日开盘价大于等于昨天最低价pass
        if today_open >= yesterday_low:
            return False
        # 今日收盘价要超过昨天实体的一半
        if today_close < yesterday_middle:
            return False

        if is_downtrend(stock):
            print(code)
            return True
        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    """
    获取沪深两市每日的斩回线形态
    """
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['signal'] = stock_df.apply(lambda x: hit_feature(x['code'], 20240221, 20240301), axis=1)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
