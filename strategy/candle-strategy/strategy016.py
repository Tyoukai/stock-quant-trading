from backtest.BaseApi import *
from sklearn.linear_model import LinearRegression
import numpy as np
import time


def hit_feature(code, start_date, end_date):
    try:
        stock = get_daily_stock_by_ak(code, start_date, end_date)
        if np.any(stock.isnull()):
            return False
        time.sleep(0.005)
        x = np.arange(len(stock.index)).reshape(-1, 1)
        stock['avg_price'] = (stock['close'] + stock['open']) / 2.0
        lr = LinearRegression().fit(x, stock['avg_price'])
        # 上涨趋势直接返回false
        if lr.coef_ >= 0:
            return False


    except Exception as e:
        return False
    pass


if __name__ == '__main__':
    """
    获取沪深两市每日的斩回线形态
    """
    stock_df = list_stock_code_and_price_by_ak(None)
