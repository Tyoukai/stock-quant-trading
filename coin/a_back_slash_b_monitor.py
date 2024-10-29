import numpy as np
from base_api import get_latest_k_line
from base_api import draw_plot_day
import datetime


def calculate_a_back_slash_b(local_df):
    local_df['a/d'] = np.zeros(len(local_df.index))
    local_df['a/d'] = (local_df['close'] - local_df['open']) / (local_df['high'] - local_df['low']) * local_df['vol']
    return local_df


if __name__ == '__main__':
    symbols = []
    for symbol in symbols:
        # 1、获取K线
        result, one_day_df = get_latest_k_line(symbol, '1d', 120, datetime.datetime.now().timestamp() * 1000)
        if not result:
            continue
        # 2、计算a/b指标
        one_day_df = calculate_a_back_slash_b(one_day_df)
        # 3、图形展示
        draw_plot_day(one_day_df, ['a/d'], symbol)
