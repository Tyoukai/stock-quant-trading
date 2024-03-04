from backtest.BaseApi import *
from sklearn.linear_model import LinearRegression
import time
import numpy as np


def up_hit_feature(code, start_date, end_date):
    """
    看涨吞没判断，当前处于下跌趋势，然后出现看涨吞没情况
    获取前5天价格，计算出斜率
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

        # 增加一个下跌天数比率参数，当下跌比率超过60%的时候，才考虑买入
        fall_count = 0.0
        total_count = len(stock.index)
        for i in range(total_count):
            open_price = stock['open'].iloc[i]
            close_price = stock['close'].iloc[i]
            if open_price > close_price:
                fall_count += 1
        if fall_count / total_count < 0.6:
            return False

        x = np.arange(len(stock.index)).reshape(-1, 1)
        stock['avg_price'] = (stock['close'] + stock['open']) / 2.0
        lr = LinearRegression().fit(x, stock['avg_price'])
        # 上涨趋势直接返回false
        if lr.coef_ >= -0.2:
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
    stock_df['signal'] = stock_df.apply(lambda x: up_hit_feature(x['code'], '20240226', '20240304'), axis=1)
    stock_df = stock_df[stock_df['signal']]
    print(stock_df)
