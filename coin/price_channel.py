import datetime
import matplotlib.pyplot as plt

from base_api import get_latest_k_line
from moving_average import ema


def show_chart(df_local):
    fig = plt.figure(1, figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.plot(ema_fifteen_minute_df['start_time'], ema_fifteen_minute_df['close'], 'r-,', label='close')
    ax.plot(ema_fifteen_minute_df['start_time'], ema_fifteen_minute_df['ema'], 'b-,', label='ema')
    ax.plot(ema_fifteen_minute_df['start_time'], ema_fifteen_minute_df['min_value'], 'g-,', label='min')
    ax.plot(ema_fifteen_minute_df['start_time'], ema_fifteen_minute_df['max_value'], 'k-,', label='max')
    ax.legend(loc=3)
    plt.show()


def calculate_coefficient(if_loop, df_local, symbol_local, coefficient_local):
    while coefficient_local < 1.0:
        df_local['min_value'] = df_local['ema'] * (1 - coefficient_local)
        df_local['max_value'] = df_local['ema'] * (1 + coefficient_local)

        count = 0.0
        for i in range(0, len(df_local.index)):
            if df_local.iloc[i]['high'] <= df_local.iloc[i]['max_value'] and \
                    df_local.iloc[i]['low'] >= df_local.iloc[i]['min_value']:
                count += 1

        if not if_loop:
            print(symbol_local, coefficient_local, count / len(df_local.index), len(df_local.index), sep=':')
            return df_local

        if count / len(df_local.index) >= 0.95:
            print(symbol_local, coefficient_local, count / len(df_local.index), len(df_local.index), sep=':')
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
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
               'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'MATICUSDT',
               'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
               'FETUSDT', 'FILUSDT']
    for symbol in symbols:
        fifteen_minute_df = get_latest_k_line(symbol, '15m', 88, int(datetime.datetime.now().timestamp() * 1000))
        fifteen_minute_df['close'] = fifteen_minute_df['close'].astype(float)
        fifteen_minute_df['low'] = fifteen_minute_df['low'].astype(float)
        fifteen_minute_df['high'] = fifteen_minute_df['high'].astype(float)
        ema_fifteen_minute_df = ema(fifteen_minute_df, 22, 'close')
        # 根据ema计算价格通道，找出符合条件的轨道系数
        ema_fifteen_minute_df = calculate_coefficient(True, ema_fifteen_minute_df, symbol, 0.0001)
        show_chart(ema_fifteen_minute_df)


