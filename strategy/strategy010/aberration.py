from backtest.BaseApi import *
from backtest.StockOperation import *
import pandas as pd
import numpy as np


def init_strategy(start_date, end_date):
    hs_300 = get_etf_inside('510300', start_date, end_date)
    hs_300 = hs_300.dropna(axis=0, how='any').reset_index(drop=True)
    df = pd.DataFrame()
    df['date'] = hs_300['净值日期']
    df['close'] = hs_300['单位净值']
    df['open'] = df['close'].shift(1)
    df['ave_value'] = np.zeros(len(df['date']))
    df['std_value'] = np.zeros(len(df['date']))
    df['up_value'] = np.zeros(len(df['date']))
    df['down_value'] = np.zeros(len(df['date']))
    df['total_asset'] = np.zeros(len(df['date']))
    df = df.dropna(axis=0, how='any').reset_index(drop=True)
    return df


if __name__ == '__main__':
    df = init_strategy('20130308', '20150413')
    length = 20
    init_fund = 100000
    cash_in_hand = 100000
    stock_num_in_hand = 0
    index = 20
    N = 2
    while index < len(df['date']):
        df['ave_value'].iloc[index] = df['close'].iloc[index - 20: index].mean()
        df['std_value'].iloc[index] = np.std(df['close'].iloc[index - 20: index], ddof=1)
        index += 1
    df['up_value'] = df['ave_value'] + N * df['std_value']
    df['down_value'] = df['ave_value'] - N * df['std_value']

    df = df.drop(range(length), axis=0).reset_index(drop=True)

    for i in range(len(df['date'])):
        if df['open'].iloc[i] > df['up_value'].iloc[i]:
            if stock_num_in_hand == 0:
                cash_in_hand, stock_num_in_hand = buy_stock(cash_in_hand, df['open'].iloc[i])
        if df['open'].iloc[i] < df['ave_value']:
            if stock_num_in_hand > 0:
                sale_stock(df['open'].iloc[i], stock_num_in_hand)








