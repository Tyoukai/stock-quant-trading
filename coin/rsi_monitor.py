import numpy as np
from base_api import get_latest_k_line
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


if __name__ == '__main__':
    """
    rsi计算法，找出当前存在价格背离的代币
    """
    # symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
    #            'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'MATICUSDT',
    #            'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
    #            'FETUSDT', 'FILUSDT', 'HBARUSDT', 'MKRUSDT', 'IMXUSDT', 'ARBUSDT', 'INJUSDT', 'VETUSDT', 'RENDERUSDT',
    #            'ATOMUSDT', 'AAVEUSDT', 'WIFUSDT', 'OPUSDT', 'ARUSDT', 'GRTUSDT', 'BONKUSDT']
    symbols = ['ETHUSDT']

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

        result, df = get_latest_k_line(symbol, interval, coin_cycle + rsi_calculate_cycle, endTime)
        if not result:
            continue
        df_rsi = calculate_rsi(df, rsi_calculate_cycle)
        # print('running')
        if hit_feature(df_rsi):
            print(symbol)
