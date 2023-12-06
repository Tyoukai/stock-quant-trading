import numpy as np
from datetime import datetime


def calculate_sharp_rate(init_fund, df, std_rate):
    """
    计算给定数据下对应的夏普率
    :param init_fund: 初始投入资金
    :param df: 策略投资详情，每日交易结束后总体资产情况。dataframe date:total_asset
    格式 日期:总体资产
    :param std_rate: 无风险年化利率
    """
    # 总的风险利率
    total_profit_rate = (df['total_asset'][-1] - init_fund) / init_fund
    df['profit'] = df['total_asset'].diff()
    df['profit'][0] = df['total_asset'][0] - init_fund
    df['profit_rate'] = df['profit'] / df['total_asset'].shift(1)
    df['profit_rate'][0] = df['profit'][0] / init_fund
    # 利率标准差
    profit_rate_std = np.std(df['profit_rate'], ddof=1)
    start_date = datetime.strptime(df.index[0], '%Y-%m-%d')
    end_date = datetime.strptime(df.index[-1], '%Y-%m-%d')
    interval = (end_date - start_date).days + 1

    # 风险收益
    erp = total_profit_rate / interval
    # 无风险收益
    rf = std_rate / 365.0
    # 标准夏普率
    return (erp - rf) / profit_rate_std


# 计算给定数据下最大回测
def calculate_max_drawdown(df):

    pass


# 计算给定数据下收益率
def calculate_rate_of_return(init_fund, df):
    return (df['total_asset'][-1] - init_fund) / init_fund

