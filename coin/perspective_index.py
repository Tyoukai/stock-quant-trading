import numpy as np
from base_api import get_latest_k_line
from moving_average import ema
import datetime
import mplfinance as mpl
import pandas as pd


def calculate_perspective_index(local_df, cycle):
    # 1、计算指定周期ema
    local_df = ema(local_df, cycle, 'close')
    # 2、计算透视指标值
    local_df['bull_power'] = local_df['high'] - local_df['ema']
    local_df['bear_power'] = local_df['low'] - local_df['ema']
    local_df = local_df.dropna(axis=0, how='any').reset_index(drop=True)
    return local_df


def draw(local_df, symbol):
    local_df['start_time'] = local_df['start_time'] / 1000
    start_time = datetime.datetime.fromtimestamp(int(local_df['start_time'][0]))
    start_time_str = datetime.datetime.strftime(start_time, '%Y%m%d')
    dates_str_list = pd.date_range(start=start_time_str, periods=len(local_df.index), freq='1d').strftime(
        '%Y-%m-%d').tolist()

    local_df.set_index(dates_str_list, inplace=True)
    add_plot = [
        mpl.make_addplot(local_df['bull_power'], type='bar', color='#00FF00', panel=1),
        mpl.make_addplot(local_df['bear_power'], type='bar', color='#FF3030', panel=2)
    ]
    my_color = mpl.make_marketcolors(up='#00FF00', down='#FF3030', inherit=True, volume='inherit')
    my_style = mpl.make_mpf_style(marketcolors=my_color, gridaxis='both', gridstyle='-.', y_on_right=False)

    mpl.plot(local_df, type='candle', datetime_format='%Y-%m-%d', style=my_style,
             mav=(7, 13, 26), addplot=add_plot, title=symbol)


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
