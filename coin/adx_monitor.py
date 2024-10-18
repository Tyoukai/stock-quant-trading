import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from base_api import get_latest_k_line
from base_api import draw_plot
from backtest.StockIndexCalculation import calculate_TR


def calculate_dm(df_local):
    """
    计算DM+ DM-
    :param df_local:
    :return:
    """
    df_local['up_move'] = df_local['high'] - df_local['high'].shift(1)
    df_local['down_move'] = df_local['low'].shift(1) - df_local['low']
    df_local['dm_plus'] = np.zeros(len(df_local.index))
    df_local['dm_minus'] = np.zeros(len(df_local.index))
    df_local = df_local.dropna(axis=0, how='any').reset_index(drop=True)
    for i in range(len(df_local.index)):
        if df_local.iloc[i]['up_move'] > max(df_local.iloc[i]['down_move'], 0):
            df_local.loc[i, 'dm_plus'] = df_local.iloc[i]['up_move']
        if df_local.iloc[i]['down_move'] > max(df_local.iloc[i]['up_move'], 0):
            df_local.loc[i, 'dm_minus'] = df_local.iloc[i]['down_move']
    return df_local


def calculate_adx(df_local, n):
    """
    计算DI值
    :param df_local:
    :param n:
    :return:
    """
    df_local['tr_n'] = np.zeros(len(df_local.index))
    df_local['dm_plus_n'] = np.zeros(len(df_local.index))
    df_local['dm_minus_n'] = np.zeros(len(df_local.index))
    df_local['di_plus_n'] = np.zeros(len(df_local.index))
    df_local['di_minus_n'] = np.zeros(len(df_local.index))

    df_local.loc[n - 1, 'tr_n'] = np.mean(df_local['TR'].iloc[0:n])
    df_local.loc[n - 1, 'dm_plus_n'] = np.mean(df_local['dm_plus'].iloc[0:n])
    df_local.loc[n - 1, 'dm_minus_n'] = np.mean(df_local['dm_minus'].iloc[0:n])

    for i in range(n, len(df_local.index)):
        df_local.loc[i, 'tr_n'] = df_local.iloc[i - 1]['tr_n'] * (n - 1) / n + df_local.iloc[i]['TR']
        df_local.loc[i, 'dm_plus_n'] = df_local.iloc[i - 1]['dm_plus_n'] * (n - 1) / n + df_local.iloc[i]['dm_plus']
        df_local.loc[i, 'dm_minus_n'] = df_local.iloc[i - 1]['dm_minus_n'] * (n - 1) / n + df_local.iloc[i]['dm_minus']
    df_local['di_plus_n'] = 100 * df_local['dm_plus_n'] / df_local['tr_n']
    df_local['di_minus_n'] = 100 * df_local['dm_minus_n'] / df_local['tr_n']
    df_local['dx'] = abs(100 * (df_local['di_plus_n'] - df_local['di_minus_n']) /
                         (df_local['di_plus_n'] + df_local['di_minus_n']))
    df_local = df_local.dropna(axis=0, how='any').reset_index(drop=True)

    df_local['adx'] = np.zeros(len(df_local.index))
    df_local.loc[n - 1, 'adx'] = np.mean(df_local['adx'].iloc[0:n])
    for i in range(n, len(df_local.index)):
        df_local.loc[i, 'adx'] = (df_local.iloc[i - 1]['adx'] * (n - 1) + df_local.loc[i]['dx']) / n
    return df_local


if __name__ == '__main__':
    # symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
    #            'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'MATICUSDT',
    #            'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
    #            'FETUSDT', 'FILUSDT']
    symbols = ['BTCUSDT']
    # 循环周期
    cycle = 13
    for symbol in symbols:
        # 1、获取指定分钟k线图
        result, fifteen_minute_df = get_latest_k_line(symbol, '15m', 120,
                                                      int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 2、计算TR
        fifteen_minute_df = calculate_TR(fifteen_minute_df)
        # 3、计算DM+ DM-
        fifteen_minute_df = calculate_dm(fifteen_minute_df)
        # 4、计算DI+ DI- DX ADX
        fifteen_minute_df = calculate_adx(fifteen_minute_df, cycle)
        # 7、图形展示
        draw_plot(fifteen_minute_df, ['di_plus_n', 'di_minus_n', 'adx'], symbol)
