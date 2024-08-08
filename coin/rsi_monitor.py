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


if __name__ == '__main__':
    client = Spot(base_url='https://api4.binance.com')
    symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'PEPEUSDT', 'WIFUSDT']
    for symbol in symbols:
        rsi_calculate_cycle = 6
        coin_cycle = 42
        current_time = datetime.datetime.now()
        startTime = int(datetime.datetime.strptime(
            (current_time - timedelta(hours=coin_cycle + rsi_calculate_cycle)).strftime('%Y-%m-%d %H'),
            '%Y-%m-%d %H').timestamp() * 1000)
        endTime = int(datetime.datetime.now().timestamp() * 1000)
        interval = '15m'
        kline = client.klines(symbol=symbol, interval=interval, startTime=startTime, endTime=endTime)

        df = pd.DataFrame(kline, columns=['start_time', 'open', 'high', 'low', 'close', 'vol', 'end_time', 'amount', 'num', '1', '2', '3'])

        df_rsi = calculate_rsi(df, rsi_calculate_cycle)
        if hit_feature(df_rsi):
            print(symbol)
