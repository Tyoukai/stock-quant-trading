# 计算股市变化的各种技术指标，如MACD、CCI、ATR等
# from BaseApi import *
import numpy as np
import matplotlib.pyplot as plt


def calculate_TR(stock_df):
    """
    计算真实波动幅度TR（true range）
    max(今日最高价 - 今日最低价, abs(今日最高价 - 昨日收盘价), abs(今日最低价 - 昨日收盘价))
    :param stock_df:
    :return:
    """
    stock_df['high_low'] = stock_df.apply(lambda x: abs(x['high'] - x['low']), axis=1)
    stock_df['close_shift'] = stock_df['close'].shift(1)
    stock_df['pre_close_high'] = stock_df.apply(lambda x: abs(x['close_shift'] - x['high']), axis=1)
    stock_df['pre_close_low'] = stock_df.apply(lambda x: abs(x['close_shift'] - x['low']), axis=1)
    stock_df['TR'] = stock_df.apply(lambda x: max(x['high_low'], x['pre_close_high'], x['pre_close_low']), axis=1)
    stock_df = stock_df.drop(['high_low', 'close_shift', 'pre_close_high', 'pre_close_low'], axis=1)
    return stock_df


def caculate_ATR(stock_df, N):
    """
    计算单只股票ATR变化情况
    :param stock_df: 股票情况，参数值：close, high, low
    :param N: 周期
    :return:
    """
    for i in range(N, len(stock_df.index)):
        stock_df['ATR'].iloc[i] = np.mean(stock_df['TR'].iloc[i-N+1:i+1])
    stock_df.drop(['close_shift', 'high_low', 'pre_close_high', 'pre_close_low', 'TR'], axis=1)
    return stock_df


def calculate_CCI(stock_df, N):
    """
    计算单只股票CCI变化情况
    :param stock_df:
    :param N: 周期
    :return:
    """
    stock_df['TP'] = np.zeros(len(stock_df.index))
    stock_df['MA'] = np.zeros(len(stock_df.index))
    stock_df['MD'] = np.zeros(len(stock_df.index))
    stock_df['CCI'] = np.zeros(len(stock_df.index))

    stock_df['TP'] = (stock_df['high'] + stock_df['low'] + stock_df['close']) / 3.0
    for i in range(N, len(stock_df.index)):
        stock_df['MA'].iloc[i] = np.mean(stock_df['close'].iloc[i-N+1:i+1])
    stock_df['MD'] = stock_df['MA'] - stock_df['close']
    for i in range(N, len(stock_df.index)):
        stock_df['MD'].iloc[i] = np.mean(stock_df['MD'].iloc[i-N+1:i+1])
    stock_df['CCI'] = (stock_df['TP'] - stock_df['MA']) / (stock_df['MD'] * 0.015)
    stock_df = stock_df.drop(['TP', 'MA', 'MD'], axis=1)
    return stock_df


def calculate_AMA(stock_df, N):
    """
    计算单只AMA指标 close 标准AMA fast：2， slow：30
    :param stock_df:
    :param N: 周期
    :return:
    """
    stock_df['close_shift'] = stock_df['close'].shift(1)
    stock_df = stock_df.dropna(axis=0, how='any').reset_index(drop=True)
    stock_df['pre_close'] = stock_df.apply(lambda x: abs(x['close'] - x['close_shift']), axis=1)
    slowest = 2.0 / (30 + 1)
    fastest = 2.0 / (2 + 1)
    stock_df['volatility'] = np.zeros(len(stock_df.index))
    stock_df['direction'] = np.zeros(len(stock_df.index))
    stock_df['ER'] = np.zeros(len(stock_df.index))
    stock_df['smooth'] = np.zeros(len(stock_df.index))
    stock_df['c'] = np.zeros(len(stock_df.index))
    stock_df['AMA'] = np.zeros(len(stock_df.index))
    for i in range(N, len(stock_df.index)):
        stock_df['volatility'].iloc[i] = sum(stock_df['pre_close'].iloc[i-N+1:i+1])
        stock_df['direction'].iloc[i] = stock_df['close'].iloc[i] - stock_df['close'].iloc[i-N+1]
    stock_df['ER'] = stock_df['direction'] / stock_df['volatility']
    stock_df['smooth'] = stock_df['ER'] * (fastest - slowest) + slowest
    stock_df['c'] = stock_df['smooth'] * stock_df['smooth']
    for i in range(N, len(stock_df.index)):
        stock_df['AMA'].iloc[i] = stock_df['AMA'].iloc[i-1] + stock_df['c'].iloc[i] * (stock_df['close'].iloc[i] - stock_df['AMA'].iloc[i-1])

    stock_df = stock_df.drop(['close_shift', 'pre_close', 'volatility', 'direction', 'ER', 'smooth', 'c'], axis=1)
    return stock_df



if __name__ == '__main__':
    # ATR计算测试
    # stock_df = get_daily_stock_by_ak('600009', '20230701', '20240105', 'hfq')
    # stock_df = caculate_ATR(stock_df, 12)
    # stock_df = stock_df.drop(range(12), axis=0)
    #
    # figure = plt.figure(1, (10, 8))
    # ax = figure.add_subplot(111)
    #
    # ax.plot(stock_df['date'], stock_df['ATR'], 'r--', label='ATR')
    # plt.legend(loc=3)
    # plt.show()

    # CCI计算测试
    # stock_df = get_daily_stock_by_ak('601318', '20230701', '20240105')
    # stock_df = calculate_CCI(stock_df, 12)
    # stock_df = stock_df.drop(range(12), axis=0)
    #
    # figure = plt.figure(1, (10, 8))
    # ax = figure.add_subplot(111)
    # ax.plot(stock_df['date'], stock_df['CCI'], 'r-', label='CCI')
    # ax.plot(stock_df['date'], np.ones(len(stock_df.index)) * 100, 'k--')
    # ax.plot(stock_df['date'], np.ones(len(stock_df.index)) * -100, 'k--')
    # plt.legend(loc=3)
    # plt.show()

    # AMA计算测试
    # stock_df = get_daily_stock_by_ak('600009', '20200701', '20240105')
    # stock_df = calculate_AMA(stock_df, 20)
    # stock_df['ma_20'] = np.zeros(len(stock_df.index))
    # for i in range(20, len(stock_df.index)):
    #     stock_df['ma_20'].iloc[i] = np.mean(stock_df['close'].iloc[i-20+1:i+1])
    #
    # figure = plt.figure(1, (10, 8))
    # ax = figure.add_subplot(111)
    # ax.plot(stock_df['date'], stock_df['close'], 'r-', label='close')
    # ax.plot(stock_df['date'], stock_df['AMA'], 'k--', label='AMA')
    # ax.plot(stock_df['date'], stock_df['ma_20'], 'g--', label='ma_12')
    # plt.legend(loc=3)
    # plt.show()
    pass



