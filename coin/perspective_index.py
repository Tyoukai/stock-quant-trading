import numpy as np
from base_api import get_latest_k_line
from moving_average import ema
import datetime


def calculate_perspective_index(local_df, cycle):
    # 1、计算指定周期ema
    local_df = ema(local_df, cycle, 'close')
    # 2、计算透视指标值
    local_df['bull_power'] = local_df['high'] - local_df['ema']
    local_df['bear_power'] = local_df['low'] - local_df['ema']
    local_df = local_df.dropna(axis=0, how='any').reset_index(drop=True)
    return local_df


def draw(local_df, symbol):
    pass


if __name__ == '__main__':
    symbols = ['']
    for symbol in symbols:
        # 1、获取制定的K线信息
        result, one_day_df = get_latest_k_line(symbol, '1d', 120, int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 2、计算透视指标
        calculated_one_day_df = calculate_perspective_index(one_day_df, 13)
        # 3、绘制图形

        pass
    pass
