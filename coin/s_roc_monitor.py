import matplotlib.pyplot as plt
import numpy as np
from moving_average import ema
from base_api import get_latest_k_line
from base_api import draw_plot_day
import datetime


def calculate_s_roc(local_df, cycle):
    """
    计算指定周期的S-RoC
    :param local_df:
    :param cycle:
    :return:
    """
    local_df['S-RoC'] = np.zeros(len(local_df.index))
    local_df['S-RoC'] = local_df['close'].shift(cycle) / local_df['close']
    local_df = local_df.dropna(axis=0, how='any').reset_index(drop=True)
    return local_df


def draw():
    pass


if __name__ == '__main__':
    # symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
    #            'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'MATICUSDT',
    #            'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
    #            'FETUSDT', 'FILUSDT']
    symbols = ['BTCUSDT']
    ema_cycle = 13
    roc_cycle = 7
    # 1、计算指定周期的EMA
    for symbol in symbols:
        result, fifteen_minute_df = get_latest_k_line(symbol, '1d', 120,
                                                      int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        fifteen_minute_df['close'] = fifteen_minute_df['close'].astype(float)
        fifteen_minute_df = ema(fifteen_minute_df, ema_cycle, 'close')
        # 2、计算S-RoC
        fifteen_minute_df = calculate_s_roc(fifteen_minute_df, roc_cycle)
        # 3、绘制图形
        draw_plot_day(fifteen_minute_df, ['S-RoC'], symbol)
