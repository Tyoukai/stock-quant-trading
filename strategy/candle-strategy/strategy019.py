from backtest.BaseApi import *
from backtest.StockShape import *
import time
import numpy as np


def hit_feature(code, start_date, end_date):
    try:
        stock = get_daily_stock_by_ak(code, start_date, end_date)
        if np.any(stock.isnull()):
            return False
        time.sleep(0.005)

        stock_len = len(stock.index)
        today_open = stock['open'].iloc[stock_len - 1]
        today_close = stock['close'].iloc[stock_len - 1]
        yesterday_open = stock['open'].iloc[stock_len - 2]
        yesterday_close = stock['close'].iloc[stock_len -2]

        # 昨天必须的跌
        if yesterday_open <= yesterday_close:
            return False
        # 今天必须是涨
        if today_open >= today_close:
            return False

        # 两天收盘价要在同一水平线，判断标准：两日价格差，小于1毛
        price_diff = abs(yesterday_close - today_close)
        if price_diff > 0.1:
            return False

        # 今天的开市价远低于昨天的收盘价,判断标准：今日实体长度是昨日实体长度的两倍以上
        today_entity = abs(today_open - yesterday_close)
        yesterday_entity = abs(yesterday_open - yesterday_close)
        if today_entity / yesterday_entity < 2.0:
            return False

        stock = stock.drop(stock_len - 1, axis=0)
        if is_downtrend(stock):
            print(code)
            return True
    except Exception as e:
        return False


if __name__ == '__main__':
    """
    反击线形态
    """
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['signal'] = stock_df.apply(lambda x: hit_feature(x['code'], '20240227', '20240305'), axis=1)
    stock_df = stock_df.dropna(axis=0, how='any').reset_index(drop=True)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
