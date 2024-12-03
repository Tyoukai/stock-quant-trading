import datetime

from base_api import get_k_line_with_start_time
from base_api import draw_one_day_with_mpl
from moving_average import ema
import mplfinance as mpl
import pandas as pd


def show_chart(df_local, symbol_local):
    df_local.index = pd.DatetimeIndex(df_local['start_time_format'])
    add_plot = [
        mpl.make_addplot(df_local['max_value'], type='line', color='g', label='up'),
        mpl.make_addplot(df_local['min_value'], type='line', color='r', label='low')
    ]
    draw_one_day_with_mpl(df_local, add_plot, symbol_local, (13), (1, 0.3))


def calculate_coefficient(if_loop, df_local, symbol_local, coefficient_local, ema_name):
    while coefficient_local < 1.0:
        df_local['min_value'] = df_local[ema_name] * (1 - coefficient_local)
        df_local['max_value'] = df_local[ema_name] * (1 + coefficient_local)

        count = 0.0
        for i in range(0, len(df_local.index)):
            if df_local.iloc[i]['high'] <= df_local.iloc[i]['max_value'] and \
                    df_local.iloc[i]['low'] >= df_local.iloc[i]['min_value']:
                count += 1

        if not if_loop:
            last_index = len(df_local.index) - 1
            print(symbol_local, coefficient_local, df_local['min_value'][last_index], df_local['max_value'][last_index],
                  df_local['close'][last_index], sep=':')
            return df_local

        if count / len(df_local.index) >= 0.95:
            last_index = len(df_local.index) - 1
            print(symbol_local, coefficient_local, df_local['min_value'][last_index], df_local['max_value'][last_index],
                  df_local['close'][last_index], sep=':')
            return df_local
        coefficient_local += 0.0001
    return df_local


if __name__ == '__main__':
    """
    价格通道，根据价格通道寻找合适的入手点
    上轨线 = EMA + EMA * 轨道系数
    下轨线 = EMA - EMA * 轨道系数
    一般要求，将近期价格点位的95%包含在轨道内部，即两倍标准差
    """
    # symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
    #            'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'MATICUSDT',
    #            'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
    #            'FETUSDT', 'FILUSDT']
    symbols = ['SUIUSDT']
    # 2024-07-03 08:00:00
    start_time = 1719964800000
    for symbol in symbols:
        result, one_day_df = get_k_line_with_start_time(symbol, start_time, '1d')
        if not result:
            continue
        calculated_one_day_df, ema_name = ema(one_day_df, 13, 'close')
        # 根据ema计算价格通道，找出符合条件的轨道系数
        calculated_one_day_df = calculate_coefficient(False, calculated_one_day_df, symbol, 0.3105999999999821, ema_name)
        show_chart(calculated_one_day_df, symbol)


