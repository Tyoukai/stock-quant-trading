from backtest.BaseApi import *
from backtest.IndexCalculation import *
from backtest.StockIndexCalculation import *
from backtest.StockOperation import *
from backtest.Graph import *
import numpy as np

if __name__ == '__main__':
    AMA_length = 20
    filter_percentage = 0.26
    # '20130308', '20150413'
    # '20190701', '20240105'
    stock_df = get_daily_stock_by_ak('600009', '20130308', '20240105')
    stock_df = calculate_AMA(stock_df, AMA_length)
    stock_df = stock_df.drop(range(120), axis=0).reset_index(drop=True)

    # 计算过滤器
    stock_df['filter'] = np.zeros(len(stock_df.index))
    for i in range(AMA_length, len(stock_df.index)):
        stock_df['filter'].iloc[i] = filter_percentage * np.std(stock_df['AMA'].iloc[i-AMA_length+1:i+1], ddof=1)
    # 计算买入卖出信号
    stock_df['AMA_shift'] = stock_df['AMA'].shift(1)
    stock_df = stock_df.drop(range(AMA_length + 1), axis=0).reset_index(drop=True)
    stock_df['signal_buy'] = np.where(stock_df['AMA'] - stock_df['AMA_shift'] > stock_df['filter'], 1, 0)
    stock_df['signal_sell'] = np.where((stock_df['AMA_shift'] - stock_df['AMA']) > stock_df['filter'], -1, 0)

    init_fund = 100000.0
    current_cash_in_hand = 100000.0
    current_stock_in_hand = 0
    stock_df['total_asset'] = np.zeros(len(stock_df.index))

    for i in range(len(stock_df)):
        if stock_df['signal_buy'].iloc[i] > 0 and current_stock_in_hand == 0:
            current_cash_in_hand, current_stock_in_hand = buy_stock(current_cash_in_hand, stock_df['close'].iloc[i])
        else:
            if stock_df['signal_sell'].iloc[i] < 0 and current_stock_in_hand > 0:
                current_cash_in_hand += sell_stock(stock_df['close'].iloc[i], current_stock_in_hand)
                current_stock_in_hand = 0
        stock_df['total_asset'].iloc[i] = current_cash_in_hand + current_stock_in_hand * stock_df['close'].iloc[i]

    calculate_sharp_rate(init_fund, stock_df, 0.03)
    calculate_max_drawdown(stock_df)
    calculate_rate_of_return(init_fund, stock_df)

    draw_return_on_assets(init_fund, stock_df)
