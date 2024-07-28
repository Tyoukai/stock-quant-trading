from binance.spot import Spot
import pandas as pd
import datetime
from datetime import timedelta


def calculate_rsi(df, rsi_calculate_cycle):
    """
    计算对应代币一段时间的rsi
    :param df:
    :param rsi_calculate_cycle:
    :return:
    """
    
    pass


def hit_feature(df):
    """
    是否命中特征
    :param df:
    :return:
    """
    pass


if __name__ == '__main__':
    client = Spot(base_url='https://api4.binance.com')
    symbols = []
    for symbol in symbols:
        rsi_calculate_cycle = 6
        coin_cycle = 42
        current_time = datetime.datetime.now()
        startTime = int(datetime.datetime.strptime(
            (current_time - timedelta(hours=coin_cycle + rsi_calculate_cycle)).strftime('%Y-%m-%d %H'),
            '%Y-%m-%d %H').timestamp() * 1000)
        endTime = int(datetime.datetime.now().timestamp() * 1000)
        interval = '1h'
        kline = client.klines(symbol=symbol, interval=interval, startTime=startTime, endTime=endTime)
        df = pd.DataFrame(kline, columns=['start_time', 'open', 'high', 'low', 'close', 'vol', 'end_time', 'amount', 'num', '1', '2', '3'])
        calculate_rsi(df, rsi_calculate_cycle)
        if hit_feature(df):
            print(symbol)