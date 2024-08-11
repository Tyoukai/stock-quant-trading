import numpy as np
from binance.spot import Spot
import pandas as pd
import datetime
from datetime import timedelta


def calculate_rsi(df_calculate, cycle):
    """
    计算对应代币一段时间的rsi
    :param df_calculate:
    :param cycle:
    :return:
    """
    df_calculate['close'] = df_calculate['close'].astype('float')
    df_calculate['cha'] = df_calculate['close'] - df_calculate['close'].shift(1)
    df_calculate['cha'] = df_calculate['cha'].fillna(0.0)
    df_calculate['rsi'] = np.zeros(len(df_calculate.index))
    for i in range(cycle - 1, len(df_calculate.index)):
        gain = 0.0
        gain_count = 0
        loss = 0.0
        loss_count = 0
        for j in range(i - cycle + 2, i + 1):
            if df_calculate.iloc[j]['cha'] > 0.0:
                gain += df_calculate.iloc[j]['cha']
                gain_count += 1
            else:
                loss += -df_calculate.iloc[j]['cha']
                loss_count += 1
        rsi = 0.0
        if loss != 0.0 and gain != 0.0:
            rs = (gain * loss_count) / (loss * gain_count)
            rsi = 100 - 100.0 / (1.0 + rs)
        elif loss == 0.0:
            rsi = 100
        elif gain == 0.0:
            rsi = 0.0
        df_calculate.loc[i, 'rsi'] = rsi
    return df.drop(range(cycle), axis=0).reset_index(drop=True)


def hit_feature(df_hit):
    """
    是否命中特征
    :param df_hit:
    :return:
    """
    current_low_price = float(df_hit.iloc[len(df_hit.index) - 1]['low'])
    current_rsi = df_hit.iloc[len(df_hit.index) - 1]['rsi']
    for i in range(0, len(df_hit.index) - 1):
        if float(df_hit.iloc[i]['low']) < current_low_price:
            return False
    for i in range(0, len(df_hit.index) - 1):
        if df_hit.iloc[i]['rsi'] < current_rsi:
            return True
    return False


def get_start_end_time(type, coin_cycle_local, rsi_calculate_cycle_local):
    """
    根据时间类型获取开始和结束时间
    :param type:
    :param coin_cycle_local:
    :param rsi_calculate_cycle_local:
    :return:
    """
    if type == '1h':
        current_time = datetime.datetime.now()
        start_time = int(datetime.datetime.strptime(
            (current_time - timedelta(hours=coin_cycle_local + rsi_calculate_cycle_local)).strftime('%Y-%m-%d %H'),
            '%Y-%m-%d %H').timestamp() * 1000)
        end_time = int(datetime.datetime.now().timestamp() * 1000)
        return start_time, end_time
    if type == '15m':
        current_time = datetime.datetime.now()
        start_time = int(datetime.datetime.strptime(
            (current_time - timedelta(minutes=(coin_cycle_local + rsi_calculate_cycle_local) * 15)).strftime('%Y-%m-%d %H:%M'),
            '%Y-%m-%d %H:%M').timestamp() * 1000)
        end_time = int(datetime.datetime.now().timestamp() * 1000)
        return start_time, end_time


def get_latest_k_line(symbol_local, interval_local, max_delta, end_time):
    """
    自定义获取指定时间段的K线
    :param symbol_local:
    :param interval_local:
    :param max_delta:
    :param end_time:
    :return:
    """
    end_time = 1723214593000
    # 计算开始时间
    if interval_local == '15m':
        unit = 15 * 60 * 1000
        tmp_end_time = end_time - end_time % unit
        start_time = tmp_end_time - unit * max_delta
        k_line = client.klines(symbol=symbol_local, interval='1m', startTime=start_time, endTime=end_time, limit=1000)
        one_minute_df = pd.DataFrame(k_line,
                          columns=['start_time', 'open', 'high', 'low', 'close', 'vol', 'end_time', 'amount', 'num',
                                   '1', '2', '3'])
        fifteen_minute_df = pd.DataFrame()
        fifteen_minute_df['start_time'] = np.zeros(max_delta + 1)
        fifteen_minute_df['start_time'] = fifteen_minute_df['start_time'].astype(int)
        fifteen_minute_df['close'] = np.zeros(max_delta + 1)
        fifteen_minute_df['close'] = fifteen_minute_df['close'].astype(str)
        fifteen_minute_df['low'] = np.zeros(max_delta + 1)
        fifteen_minute_df['low'] = fifteen_minute_df['low'].astype(str)
        for i in range(max_delta + 1):
            tmp_one_minute_df = pd.DataFrame()
            if i == max_delta:
                tmp_one_minute_df = one_minute_df.iloc[i * 15: len(one_minute_df.index)]
            else:
                tmp_one_minute_df = one_minute_df[i * 15: i * 15 + 15]
            min_low = tmp_one_minute_df['low'].min()
            close = tmp_one_minute_df['close'].iloc[len(tmp_one_minute_df.index) - 1]
            start_time = tmp_one_minute_df['start_time'].iloc[0]
            fifteen_minute_df.loc[i, 'start_time'] = start_time
            fifteen_minute_df.loc[i, 'close'] = close
            fifteen_minute_df.loc[i, 'low'] = min_low
        return fifteen_minute_df
    return pd.DataFrame()


if __name__ == '__main__':
    client = Spot(base_url='https://api4.binance.com')
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT', 'TRXUSDT',
               'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'MATICUSDT',
               'UNIUSDT', 'PEPEUSDT', 'ICPUSDT']
    for symbol in symbols:
        interval = '15m'
        rsi_calculate_cycle = 6
        coin_cycle = 42
        startTime, endTime = get_start_end_time('15m', coin_cycle, rsi_calculate_cycle)
        # interval = '1h'
        # rsi_calculate_cycle = 6
        # coin_cycle = 42
        # startTime, endTime = get_start_end_time('1h', 36, 6)
        # kline = client.klines(symbol=symbol, interval=interval, startTime=startTime, endTime=endTime)
        # df = pd.DataFrame(kline, columns=['start_time', 'open', 'high', 'low', 'close', 'vol', 'end_time', 'amount', 'num', '1', '2', '3'])

        df = get_latest_k_line(symbol, interval, coin_cycle + rsi_calculate_cycle, endTime)
        df_rsi = calculate_rsi(df, rsi_calculate_cycle)
        if hit_feature(df_rsi):
            print(symbol)
