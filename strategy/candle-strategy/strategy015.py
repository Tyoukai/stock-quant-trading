from backtest.BaseApi import *
from backtest.StockShape import *
import time
import numpy as np


def up_hit_feature(code, start_date, end_date):
    """
    看涨吞没判断，当前处于下跌趋势，然后出现看涨吞没情况
    判断当前是否是吞没形态
    :param code:
    :param start_date:
    :param end_date:
    :return:
    """
    try:
        stock = get_daily_stock_by_ak(code, start_date, end_date)
        if np.any(stock.isnull()):
            return False
        time.sleep(0.005)

        today_index = len(stock.index) - 1
        yesterday_index = today_index - 1
        yesterday_open = stock['open'].iloc[yesterday_index]
        yesterday_close = stock['close'].iloc[yesterday_index]
        today_open = stock['open'].iloc[today_index]
        today_close = stock['close'].iloc[today_index]

        # 昨天涨，今天跌，pass
        if yesterday_open <= yesterday_close or today_open >= today_close:
            return False

        # 今天未包含昨天的实体，pass
        if not (today_open < yesterday_close and today_close > yesterday_open):
            return False

        stock = stock.drop(len(stock.index) - 1, axis=0)
        if is_downtrend(stock):
            print(code)
            return True
        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    """
        吞没形态判断
            找出看涨吞没以及看跌吞没
    """
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['signal'] = stock_df.apply(lambda x: up_hit_feature(x['code'], '20240307', '20240314'), axis=1)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
