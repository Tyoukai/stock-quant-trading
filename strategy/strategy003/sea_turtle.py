from backtest.BaseApi import *
from backtest.StockOperation import *
from backtest.IndexCalculation import *
from backtest.Graph import *
import numpy as np


if __name__ == '__main__':
    stock_df = get_daily_stock_by_ak('600009', '20130308', '20240105')
    buy_N = 5
    sell_N = 10

    stock_df['up'] = stock_df['high'].rolling(buy_N, closed='right').max()
    stock_df['down'] = stock_df['low'].rolling(sell_N, closed='right').max()
    stock_df = stock_df.dropna(axis=0, how='any').reset_index(drop=True)

    stock_df['signal_buy'] = np.zeros(len(stock_df.index))
    stock_df['signal_sell'] = np.zeros(len(stock_df.index))
    stock_df['signal_buy'] = np.where(stock_df['up'] < stock_df['close'], 1, 0)
    stock_df['signal_sell'] = np.where(stock_df['down'] > stock_df['close'], 1, 0)

    init_fund = 100000.0
    current_cash_in_hand = 100000.0
    current_stock_in_hand = 0
    stock_df['total_asset'] = np.zeros(len(stock_df.index))

    for i in range(len(stock_df.index)):
        if stock_df['signal_buy'].iloc[i] > 0 and current_stock_in_hand == 0:
            current_cash_in_hand, current_stock_in_hand = buy_stock(current_cash_in_hand, stock_df['close'].iloc[i])
        else:
            if stock_df['signal_sell'].iloc[i] > 0 and current_stock_in_hand > 0:
                current_cash_in_hand += sell_stock(stock_df['close'].iloc[i], current_stock_in_hand)
                current_stock_in_hand = 0
        stock_df['total_asset'].iloc[i] = current_cash_in_hand + current_stock_in_hand * stock_df['close'].iloc[i]

    calculate_sharp_rate(init_fund, stock_df, 0.03)
    calculate_rate_of_return(init_fund, stock_df)
    calculate_rate_of_return(init_fund, stock_df)

    draw_return_on_assets(init_fund, stock_df)
