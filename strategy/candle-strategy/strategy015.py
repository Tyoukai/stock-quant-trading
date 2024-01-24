from backtest.BaseApi import *
from datetime import date
from datetime import timedelta


def up_hit_feature(code, days):
    """
    看涨吞没判断，当前处于下跌趋势，然后出现看涨吞没情况
    获取前5天价格，计算出斜率
    判断当前是否是吞没形态
    :param code:
    :return:
    """
    current_date = date.today().strftime('%Y%m%d')
    days_age = (date.today() - timedelta(days)).strftime('%Y%m%d')
    stock = get_daily_stock_by_ak(code, days_age, current_date)
    pass


if __name__ == '__main__':
    """
        吞没形态判断
            找出看涨吞没以及看跌吞没
    """
    stock_df = list_stock_code_and_price_by_ak(None)

    pass


