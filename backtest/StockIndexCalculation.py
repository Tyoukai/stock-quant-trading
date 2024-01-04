# 计算股市变化的各种技术指标，如MACD、CCI、ATR等

import numpy as np
import pandas as pd


def caculate_ATR(stock_df, N):
    """
    计算单只股票ATR变化情况
    :param stock_df: 股票情况，参数值：close, high, low
    :param N: 周期
    :return:
    """
    stock_df['high_low'] = stock_df.apply(abs(stock_df['high'] - stock_df['low']), axis=1)
    stock_df['pre_close_high'] = stock_df.apply(abs(stock_df['close'] - stock_df['high'].shift(1)), axis=1)
    stock_df['pre_close_low'] = stock_df.apply(abs(stock_df['close'] - stock_df['low'].shift(1)), axis=1)
    stock_df['TR'] = stock_df.apply(min(stock_df['high_low'], stock_df['pre_close_high'], stock_df['pre_close_low']), axis=1)
    stock_df['ATR'] = np.zeros(len(stock_df.index))

    for i in range(N, len(stock_df.index)):
        stock_df['ATR'].iloc[i] = sum(stock_df.iloc[N-i:N]) / N

    return stock_df


def calculate_CCI(stock_df, N):
    """
    计算单只股票CCI变化情况
    :param stock_df:
    :param N:
    :return:
    """
    pass
