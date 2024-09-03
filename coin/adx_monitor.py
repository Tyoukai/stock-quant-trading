import numpy as np
import datetime

from base_api import get_latest_k_line
from backtest.StockIndexCalculation import calculate_TR


def calculate_dm(df_local):
    """
    计算DM+ DM-
    :param df_local:
    :return:
    """
    df_local['up_move'] = df_local['high'] - df_local['high'].shift(1)
    df_local['down_move'] = df_local['low'].shift(-1) - df_local['low']
    df_local['dm+'] = np.zeros(len(df_local.index))
    df_local['dm-'] = np.zeros(len(df_local.index))
    for i in range(len(df_local.index)):
        if df_local.iloc[i]['up_move'] > max(df_local.iloc[i]['down_move'], 0):
            df_local.loc[i, 'dm+'] = df_local.iloc[i]['up_move']
        if df_local.iloc[i]['down_move'] > max(df_local.iloc[i]['up_move'], 0):
            df_local.loc[i, 'dm-'] = df_local.iloc[i]['down_move']
    return df_local


def draw(df_local):
    pass


if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
               'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'MATICUSDT',
               'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
               'FETUSDT', 'FILUSDT']
    # 循环周期
    cycle = 13
    for symbol in symbols:
        # 1、获取指定分钟k线图
        result, fifteen_minute_df = get_latest_k_line(symbol, '15m', 67,
                                                      int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 2、计算TR
        fifteen_minute_df = calculate_TR(fifteen_minute_df)
        # 3、计算DM+ DM-
        fifteen_minute_df = calculate_dm(fifteen_minute_df)
        # 4、计算DI+ DI-
        # 5、计算DX
        # 6、计算ADX
        # 7、图形展示
        draw(fifteen_minute_df)
