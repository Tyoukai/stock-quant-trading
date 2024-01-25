from backtest.BaseApi import *
from datetime import date
from datetime import timedelta
from sklearn.linear_model import LinearRegression
import time
import numpy as np


def up_hit_feature(code, days):
    """
    看涨吞没判断，当前处于下跌趋势，然后出现看涨吞没情况
    获取前5天价格，计算出斜率
    判断当前是否是吞没形态
    :param code:
    :param days:
    :return:
    """
    current_date = date.today().strftime('%Y%m%d')
    days_age = (date.today() - timedelta(days)).strftime('%Y%m%d')
    stock = get_daily_stock_by_ak(code, days_age, current_date)
    time.sleep(0.005)
    x = np.arange(len(stock.index)).reshape(-1, 1)
    stock['avg_price'] = (stock['close'] + stock['open']) / 2.0
    lr = LinearRegression().fit(x, stock['avg_price'])
    # 上涨趋势直接返回false
    if lr.coef_ >= 0:
        return False

    today_index = len(stock.index) - 1
    yesterday_index = today_index - 1
    yesterday_open = stock['open'].iloc[yesterday_index]
    yesterday_close = stock['close'].iloc[yesterday_index]
    today_open = stock['open'].iloc[today_index]
    today_close = stock['close'].iloc[today_index]

    if yesterday_open <= yesterday_close or today_open >= today_close:
        return False

    if today_open < yesterday_close and today_close > yesterday_open:
        return True
    return False


if __name__ == '__main__':
    """
        吞没形态判断
            找出看涨吞没以及看跌吞没
    """
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['signal'] = stock_df.apply(lambda x: up_hit_feature(x['code'], 5), axis=1)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
