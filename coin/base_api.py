import numpy as np
from binance.spot import Spot
import pandas as pd
import datetime
from datetime import timedelta


def get_latest_k_line(symbol_local, interval_local, max_delta, end_time):
    """
    自定义获取指定时间段的K线
    :param symbol_local: 代币符号
    :param interval_local: 15m:15分钟，1h：1小时
    :param max_delta: 想要获取多少个interval_local时间维度的k线
    :param end_time:
    :return:
    """
    client = Spot(base_url='https://api4.binance.com')
    # 计算开始时间
    if interval_local == '15m':
        length = max_delta * 15
        one_minute_unit = 60 * 1000
        unit = 15 * 60 * 1000
        end_time = end_time - end_time % one_minute_unit
        start_time = end_time - end_time % unit - unit * max_delta
        one_minute_df = None
        for i in range(0, length // 1000 + 1):
            tmp_start_time = start_time + i * 1000 * one_minute_unit
            tmp_end_time = 0
            if i == length // 1000:
                tmp_end_time = end_time
            else:
                tmp_end_time = start_time + i * 1000 * one_minute_unit + 1000 * one_minute_unit
            k_line = None
            try:
                k_line = client.klines(symbol=symbol_local, interval='1m', startTime=tmp_start_time,
                                       endTime=tmp_end_time,
                                       limit=1000)
            except BaseException:
                return False, pd.DataFrame()
            one_shard_minute_df = pd.DataFrame(k_line, columns=['start_time', 'open', 'high', 'low', 'close', 'vol',
                                                                'end_time', 'amount', 'num', '1', '2', '3'])
            if one_minute_df is None:
                one_minute_df = one_shard_minute_df
            else:
                one_minute_df = one_minute_df._append(one_shard_minute_df)

        one_minute_df = one_minute_df.reset_index(drop=True)
        fifteen_minute_df = pd.DataFrame()
        fifteen_minute_df['start_time'] = np.zeros(max_delta + 1)
        fifteen_minute_df['start_time'] = fifteen_minute_df['start_time'].astype(int)
        fifteen_minute_df['close'] = np.zeros(max_delta + 1)
        fifteen_minute_df['low'] = np.zeros(max_delta + 1)
        fifteen_minute_df['high'] = np.zeros(max_delta + 1)
        for i in range(max_delta + 1):
            tmp_one_minute_df = pd.DataFrame()
            if i == max_delta:
                tmp_one_minute_df = one_minute_df.iloc[i * 15: len(one_minute_df.index)]
            else:
                tmp_one_minute_df = one_minute_df[i * 15: i * 15 + 15]
            tmp_one_minute_df_low = (tmp_one_minute_df[['low']].copy()).astype('float')
            tmp_one_minute_df_close = (tmp_one_minute_df[['close']].copy()).astype('float')
            tmp_one_minute_df_high = (tmp_one_minute_df[['high']].copy()).astype('float')
            min_low = tmp_one_minute_df_low['low'].min()
            close = tmp_one_minute_df_close['close'].iloc[len(tmp_one_minute_df.index) - 1]
            high = tmp_one_minute_df_high['high'].iloc[len(tmp_one_minute_df.index) - 1]
            start_time = tmp_one_minute_df['start_time'].iloc[0]
            fifteen_minute_df.loc[i, 'start_time'] = start_time
            fifteen_minute_df.loc[i, 'close'] = close
            fifteen_minute_df.loc[i, 'high'] = high
            fifteen_minute_df.loc[i, 'low'] = min_low
        fifteen_minute_df['close'] = fifteen_minute_df['close'].astype(str)
        fifteen_minute_df['low'] = fifteen_minute_df['low'].astype(str)
        fifteen_minute_df['high'] = fifteen_minute_df['high'].astype(str)
        return True, fifteen_minute_df
    return False, pd.DataFrame()
