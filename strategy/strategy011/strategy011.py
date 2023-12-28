from backtest.BaseApi import *
from backtest.StockOperation import *
from backtest.IndexCalculation import *
from backtest.Graph import *

import numpy as np


def caluclate_macd(stock_list, start_date, end_date):

    # 计算macd
    stocks_daily_close = pd.DataFrame()
    for index in range(len(stock_list)):
        stock_daily_price = get_daily_stock_by_ak(stock_list[index], start_date, end_date)
        if index == 0:
            stocks_daily_close['date'] = stock_daily_price['date']
        stocks_daily_close[str(stock_list[index])] = df['close']
        stocks_daily_close['hold_' + str(stock_list[index])] = np.zeros(len(stocks_daily_close))
        stocks_daily_close['cost_' + str(stock_list[index])] = np.zeros(len(stocks_daily_close))
        index += 1
    hs_300_etf = get_etf_inside('510300', start_date, end_date)
    zz_500_etf = get_etf_inside('510500', start_date, end_date)
    stocks_daily_close['close_300'] = hs_300_etf['单位净值']
    stocks_daily_close['close_500'] = zz_500_etf['单位净值']
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
    return stocks_daily_close


def sell_all_stocks():
    pass


if __name__ == '__main__':

    start_date = '20130308'
    end_date = '20150413'
    num = 10
    init_fund = 100000
    cash_in_hand = 100000


    # 1、获取前num个的低价股
    df = list_stock_code_and_price(None)
    hs_300_stock_code = get_stock_constituent_by_ak('000300')
    df = df[df['code'] in hs_300_stock_code]
    df = df.sort_values(by=['close'], ascending=[True]).iloc[num]
    stock_num_in_hand = pd.DataFrame(columns=df['code'])

    # 2、计算低价股的macd指标&入场信号
    stocks_daily_close = caluclate_macd(df['code'], start_date, end_date)
    stocks_daily_close = stocks_daily_close.iloc[30:].reset_index(drop=True)
    for index in range(20, len(stocks_daily_close.index)):
        increase_300 = (stocks_daily_close['close_300'].iloc[index] - stocks_daily_close['close_300'].iloc[index - 20]) / stocks_daily_close['close_300'].iloc[index - 20]
        increase_500 = (stocks_daily_close['close_500'].iloc[index] - stocks_daily_close['close_500'].iloc[index - 20]) / stocks_daily_close['close_300'].iloc[index - 20]
        if increase_300 < 0 and increase_500 < 0:
            # 卖出所有的股票
            for code in df['code']:
                cash_in_hand += stock_num_in_hand[code].iloc[0] * stocks_daily_close['close_' + code].iloc[index]
                stocks_daily_close['cost_' + code].iloc[index] = 0
                stocks_daily_close['hold_' + code].iloc[index] = 0
            continue
        # 1、计算是否买股票
        for code in df['code']:
            if stocks_daily_close['signal_' + code].iloc[index] == 1 and stocks_daily_close['hold_' + code].iloc[index] == 0:
                buy_stock_cash = cash_in_hand * 0.1
                left_cash, stock_in_hand = buy_stock(buy_stock_cash, stocks_daily_close['close_' + code])
                if stock_in_hand == 0:
                    stocks_daily_close['cost_' + code].iloc[index] = 0
                    stocks_daily_close['hold_' + code].iloc[index] = 0
                    continue
                cash_in_hand = cash_in_hand * 0.9 + left_cash
                stock_num_in_hand[code].iloc[0] = stock_in_hand
                stocks_daily_close['cost_' + code].iloc[index] = buy_stock_cash - left_cash
                stocks_daily_close['hold_' + code].iloc[index] = 1
                continue
            # 判断是否卖股票
            if stocks_daily_close['hold_' + code].iloc[index] == 1:
                current_value = stock_num_in_hand[code].iloc[0] * stocks_daily_close['close_' + code].iloc[index]
                increase_rate = (current_value - stocks_daily_close['cost_' + code].iloc[index - 1]) / stocks_daily_close['cost_' + code].iloc[index - 1]
                if increase_rate >= 0.2 or increase_rate < -0.1:
                    cash_in_hand += current_value
                    stocks_daily_close['hold_' + code].iloc[index] = 0
                    stocks_daily_close['cost_' + code].iloc[index] = 0
                    continue
            # 复制之前的参数变量
            stocks_daily_close['cost_' + code].iloc[index] = stocks_daily_close['cost_' + code].iloc[index - 1]
            stocks_daily_close['hold_' + code].iloc[index] = stocks_daily_close['hold_' + code].iloc[index - 1]

        # 计算总资产
        total_assert = cash_in_hand
        for code in df['code']:
            total_assert += stock_num_in_hand[code].iloc[0] * stocks_daily_close['close_' + code].iloc[index]
        stocks_daily_close['total_assert'].iloc[index] = total_assert

    calculate_sharp_rate(init_fund, stocks_daily_close, 0.03)
    calculate_max_drawdown(df)
    draw_return_on_assets(init_fund, stocks_daily_close)
