import pandas as pd

from backtest.BaseApi import *

import numpy as np


def caluclate_macd(stock_list, start_date, end_date):

    # 计算macd
    stocks_daily_close = pd.DataFrame()
    for index in range(len(stock_list)):
        stock_daily_price = get_daily_stock_by_ak(stock_list[index], start_date, end_date)
        if index == 0:
            stocks_daily_close['date'] = stock_daily_price['date']
        stocks_daily_close[str(stock_list[index])] = df['close']
        index += 1
    stocks_daily_close = stocks_daily_close.dropna(axis=0, how='any').reset_index(drop=True)
    stocks_daily_close.iloc[0] = np.zeros(len(stock_list))
    for code in stock_list:
        stocks_daily_close['EMA12_' + code] = np.zeros(len(stocks_daily_close.index))
        stocks_daily_close['EMA26_' + code] = np.zeros(len(stocks_daily_close.index))
        stocks_daily_close['DIF_' + code] = np.zeros(len(stocks_daily_close.index))
        stocks_daily_close['DEA_' + code] = np.zeros(len(stocks_daily_close.index))
        stocks_daily_close['signal_' + code] = np.zeros(len(stocks_daily_close.index))

    for index in range(1, len(stocks_daily_close.index)):
        for code in stock_list:
            stocks_daily_close['EMA12_' + code].iloc[index] = 2 * stocks_daily_close['close'].iloc[index] / (12 + 1) + 11 * stocks_daily_close['EMA12_' + code].iloc[index - 1] / (12 + 1)
            stocks_daily_close['EMA26_' + code].iloc[index] = 2 * stocks_daily_close['close'].iloc[index] / (26 + 1) + 25 * stocks_daily_close['EMA26_' + code].iloc[index - 1] / (26 + 1)
            stocks_daily_close['DIF_' + code].iloc[index] = stocks_daily_close['EMA12_' + code].iloc[index] - stocks_daily_close['EMA26_' + code].iloc[index]
            stocks_daily_close['DEA_' + code].iloc[index] = 2 / (9 + 1) * stocks_daily_close['DIF_' + code].iloc[index] + 8 / (9 + 1) * stocks_daily_close['DEA_' + code].iloc[index - 1]

    # 计算入场信号
    for code in stock_list:
        stocks_daily_close['signal_' + code] = np.where(stocks_daily_close['DIF_' + code] - stocks_daily_close['DEA_' + code] > 0, 1, 0)


if __name__ == '__main__':

    start_date = ''
    end_date = ''
    num = 10

    # 1、获取前10的低价股
    df = list_stock_code_and_price(num)
    ave_close = df['close'].mean()
    df = df[ave_close > df['close'] > 1]
    df = df.sort_values(by=['close'], ascending=[True]).iloc[10]

    # 2、计算低价股的macd指标
    caluclate_macd(df)
    # 3、计算入场信号
    
    # 4、计算策略效果