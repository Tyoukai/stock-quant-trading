import numpy as np
from base_api import get_latest_k_line
from base_api import draw_one_day_with_mpl
import datetime
import mplfinance as mpl
import pandas as pd


def calculate_a_back_slash_b(local_df):
    local_df['a/d'] = np.zeros(len(local_df.index))
    local_df['a/d'] = (local_df['close'] - local_df['open']) / (local_df['high'] - local_df['low']) * local_df['volume']
    return local_df


def draw(local_df, local_symbol):
    local_df.index = pd.DatetimeIndex(local_df['start_time_format'])
    add_plot = [
        mpl.make_addplot(local_df['a/d'], type='line', color='k', panel=1, label='a/d')
    ]
    draw_one_day_with_mpl(local_df, add_plot, local_symbol, (13), (1, 0.5))


if __name__ == '__main__':
    """
    a/d指标
    """
    symbols = ['PEPEUSDT']
    for symbol in symbols:
        # 1、获取K线
        result, one_day_df = get_latest_k_line(symbol, '1d', 120, int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 2、计算a/b指标
        one_day_df = calculate_a_back_slash_b(one_day_df)
        # 3、图形展示
        draw(one_day_df, symbol)
