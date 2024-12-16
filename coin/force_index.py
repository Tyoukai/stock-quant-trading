import mplfinance as mpl
import numpy as np
from base_api import get_latest_k_line
from base_api import draw_one_day_with_mpl
import datetime
from moving_average import ema
import pandas as pd


def calculate_force_index(local_df):
    local_df['force_index'] = local_df['volume'] * (local_df['close'] - local_df['close'].shift(1))
    local_df = local_df.dropna(axis=0, how='any').reset_index(drop=True)
    local_df, ema_name_2 = ema(local_df, 2, 'force_index')
    local_df, ema_name_13 = ema(local_df, 13, 'force_index')
    return local_df


def draw(local_df, symbol):
    local_df.index = pd.DatetimeIndex(local_df['start_time_format'])
    add_plot = [
        mpl.make_addplot(local_df['force_index_2_ema'], type='line', color='k', panel=1, label='ema2'),
        # mpl.make_addplot(np.zeros(len(local_df.index)), type='line', color='k', panel=1, y_on_right=False),
        mpl.make_addplot(local_df['force_index_13_ema'], type='line', color='g', panel=2, label='ema13'),
        # mpl.make_addplot(np.zeros(len(local_df.index)), type='line', color='k', panel=2, y_on_right=False)
    ]
    draw_one_day_with_mpl(local_df, add_plot, symbol, (13), (1, 0.5, 0.5))


if __name__ == '__main__':
    """
    劲道指数
    """
    symbols = ['PEPEUSDT', 'ETCUSDT']
    # symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
    #            'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT',
    #            'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
    #            'FETUSDT', 'FILUSDT']
    for symbol in symbols:
        # 1、获取制定的K线信息
        result, one_day_df = get_latest_k_line(symbol, '1d', 120, int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 2、计算劲道指数
        calculated_one_day_df = calculate_force_index(one_day_df)
        # 3、绘制图形
        draw(calculated_one_day_df, symbol)
