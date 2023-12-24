from backtest.BaseApi import *

import numpy as np


def caluclate_macd(df):
    pass


if __name__ == '__main__':
    # 1、获取低价股
    df = list_low_price_stock(10)
    # 2、计算低价股的macd指标
    caluclate_macd(df)
    # 3、计算入场信号
    
    # 4、计算策略效果