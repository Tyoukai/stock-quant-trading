from backtest.BaseApi import *
from backtest.IndexCalculation import *
from backtest.StockIndexCalculation import *
import numpy as np

if __name__ == '__main__':
    AMA_length = 20
    filter_percentage = 0.26
    filter_length = 12
    stock_df = get_daily_stock_by_ak('600009', '20200701', '20240105')
    stock_df = calculate_AMA(stock_df, AMA_length)
    stock_df = stock_df.drop(range(120), axis=0).reset_index(drop=True)

    # 计算过滤器
    stock_df['filter'] = np.zeros(len(stock_df.index))
    for i in range(AMA_length, len(stock_df.index)):
        stock_df['filter'].iloc[i] = filter_percentage * np.std(stock_df['AMA'].iloc[i-AMA_length+1:i+1], ddof=1)

    # 计算买入卖出信号
