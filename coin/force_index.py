import mplfinance as mpl
import numpy as np
import pandas as pd
from base_api import get_latest_k_line


def calculate_force_index(local_df, symbol):
    pass


def draw(local_df, symbol):
    pass


if __name__ == '__main__':
    symbols = ['BTCUSDT']
    for symbol in symbols:
        # 1、获取制定的K线信息
        result, one_day_df = get_latest_k_line(symbol, '1d', 120, int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 2、计算劲道指数
        calculated_one_day_df = calculate_force_index(one_day_df, symbol)
        # 3、绘制图形
        draw(calculated_one_day_df, symbol)