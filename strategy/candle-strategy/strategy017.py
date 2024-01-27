from backtest.BaseApi import *
from datetime import date
from datetime import timedelta
import time


def hit_feature(code):
    today = date.today().strftime('%Y%M%d')
    six_days_age = (date.today() - timedelta(6)).strftime('%Y%M%d')
    stock = get_daily_stock_by_ak(code, six_days_age, today)



    pass


if __name__ == '__main__':
    """
    启明星形态判断
        找出看涨的反转趋势图
    """

    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['star_signal'] = stock_df.apply(lambda x: hit_feature(x['code']), axis=1)
    stock_df = stock_df[stock_df['star_signal']]
    print(stock_df)