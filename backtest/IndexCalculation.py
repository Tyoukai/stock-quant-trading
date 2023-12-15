import numpy as np
import datetime
import pandas as pd


def calculate_sharp_rate(init_fund, df, std_rate):
    """
    计算给定数据下对应的夏普率
    :param init_fund: 初始投入资金
    :param df: 策略投资详情，每日交易结束后总体资产情况。dataframe date:total_asset
    格式 日期:总体资产
    :param std_rate: 无风险年化利率
    """
    # 总的风险利率
    total_profit_rate = (df['total_asset'].iloc[-1] - init_fund) * 1.0 / init_fund
    df['profit'] = df['total_asset'].diff()
    df.loc[0, 'profit'] = df['total_asset'][0] - init_fund
    df['profit_rate'] = df['profit'] / df['total_asset'].shift(1)
    df.loc[0, 'profit_rate'] = df['profit'][0] * 1.0 / init_fund
    # 利率标准差
    profit_rate_std = np.std(df['profit_rate'], ddof=1)
    interval = 1
    if isinstance(df['date'][0], datetime.date) or isinstance(df['date'][0], datetime.datetime):
        interval = (df['date'].iloc[-1] - df['date'][0]).days + 1
    else:
        start_date = datetime.datetime.strptime(df['date'][0], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(df['date'].iloc[-1], '%Y-%m-%d')
        interval = (end_date - start_date).days + 1

    # 风险收益
    erp = total_profit_rate / interval
    # 无风险收益
    rf = std_rate / 356
    # 标准夏普率
    sharp_rate = (erp - rf) / profit_rate_std
    print('夏普率:', sharp_rate)
    return sharp_rate


# 计算给定数据下最大回测
def calculate_max_drawdown(df):
    max_drawdown = 0
    total_asset = df['total_asset']

    count = len(total_asset)
    for index in range(count - 1):
        for index1 in range(index + 1, count):
            if total_asset[index] > total_asset[index1]:
                tmp_max_drawdown = 1 - total_asset[index1] * 1.0 / total_asset[index]
                if tmp_max_drawdown > max_drawdown:
                    max_drawdown = tmp_max_drawdown
    print('最大回撤:', max_drawdown)
    return max_drawdown


# 计算给定数据下收益率
def calculate_rate_of_return(init_fund, df):
    df['rate_of_return'] = (df['total_asset'] - init_fund) * 1.0 / init_fund


if __name__ == '__main__':
    df = pd.DataFrame({
        'date': ['2023-11-27', '2023-11-28', '2023-11-29', '2023-11-30', '2023-12-01', '2023-12-02'],
        'total_asset': [5500, 4900, 4200, 4600, 5400, 5500]
    })
    print(calculate_sharp_rate(5000.0, df, 0.03))
    print(calculate_max_drawdown(df))
    print(calculate_rate_of_return(5000.0, df))

