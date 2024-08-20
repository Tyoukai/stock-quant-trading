import datetime
import numpy as np
import matplotlib.pyplot as plt

from base_api import get_latest_k_line
from moving_average import ema


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
        fifteen_minute_df = get_latest_k_line(symbol, '15m', 66, int(datetime.datetime.now().timestamp() * 1000))
        fifteen_minute_df['close'] = fifteen_minute_df['close'].astype(float)
        fifteen_minute_df['low'] = fifteen_minute_df['low'].astype(float)
        fifteen_minute_df['high'] = fifteen_minute_df['high'].astype(float)
        ema_fifteen_minute_df = ema(fifteen_minute_df, 6, 'close')
        # 根据ema计算价格通道，找出符合条件的轨道系数
        catch_95 = False
        for coefficient in np.linspace(0, 1, 30):
            ema_fifteen_minute_df['min_value'] = ema_fifteen_minute_df['ema'] * (1 - coefficient)
            ema_fifteen_minute_df['max_value'] = ema_fifteen_minute_df['ema'] * (1 + coefficient)
            tmp_df_value = ema_fifteen_minute_df[ema_fifteen_minute_df['high'] <= ema_fifteen_minute_df['max_value'] &
                                                 ema_fifteen_minute_df['low'] >= ema_fifteen_minute_df['min_value']]
            if len(tmp_df_value.index) / len(ema_fifteen_minute_df.index) >= 0.95:
                catch_95 = True
                break

        if catch_95:
            fig = plt.figure(1, figsize=(6, 4))
            ax = fig.add_subplot(111)
            ax.plot(ema_fifteen_minute_df['start_time'], ema_fifteen_minute_df['close'], 'r-.d', label='close')
            ax.plot(ema_fifteen_minute_df['start_time'], ema_fifteen_minute_df['ema'], 'b-.d', label='ema')
            ax.plot(ema_fifteen_minute_df['start_time'], ema_fifteen_minute_df['min_value'], 'g-.d', label='min')
            ax.plot(ema_fifteen_minute_df['start_time'], ema_fifteen_minute_df['max_value'], 'g-.d', label='max')
            ax.legend(loc=3)
            plt.show()
