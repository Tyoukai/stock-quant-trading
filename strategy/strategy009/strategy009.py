import numpy as np

from backtest.BaseApi import get_etf_inside
from backtest.IndexCalculation import *
import pandas as pd


def init_strategy():
    """
    初始化策略
    :return:
    """
    # 上证50ETF 510050  start 2013-03-08
    # 沪深300ETF 510300 start 2013-03-08
    # 中证500ETF 510500 start 2013-03-08
    # 国债指数ETF 511010 start 2013-03-08

    sz_50_etf = get_etf_inside('510050', '20231120', '20231208')
    hs_300_etf = get_etf_inside('510300', '20231120', '20231208')
    zz_500_etf = get_etf_inside('510500', '20231120', '20231208')
    gz_etf = get_etf_inside('511010', '20231120', '20231208')
    # sz_50_etf = sz_50_etf.reindex(sz_50_etf.index[::-1]).reset_index(drop=True)
    # hs_300_etf = hs_300_etf.reindex(hs_300_etf.index[::-1]).reset_index(drop=True)
    # zz_500_etf = zz_500_etf.reindex(zz_500_etf.index[::-1]).reset_index(drop=True)
    # gz_etf = gz_etf.reindex(gz_etf.index[::-1]).reset_index(drop=True)

    df = pd.DataFrame()
    df['date'] = sz_50_etf['净值日期']
    df['close_50'] = sz_50_etf['单位净值']
    df['close_300'] = hs_300_etf['单位净值']
    df['close_500'] = zz_500_etf['单位净值']
    df['close_gz'] = gz_etf['单位净值']
    df['total_asset'] = np.zeros(len(df['date']))
    return df


def buy_stock(current_cash, price):
    """
    买指定股票熟料
    :param current_cash: 当前手持现金数量
    :param price: 当前股票的价格
    :return: 剩余现金数量，手持股票数量
    """
    stock_in_hand = current_cash // price
    left_cash = current_cash - price * stock_in_hand
    return left_cash, stock_in_hand


def sale_stock(price, stock_num):
    """
    卖股票
    :param price:
    :param stock_num:
    :return:
    """
    return price * stock_num


if __name__ == '__main__':
    df = init_strategy()
    init_fund = 100000.0
    current_cash = 100000.0
    current_etf_num = 0
    current_hold = ''
    i = 10
    period = 10
    while i < df.index[-1]:

        # 计算当前周期内的总资产
        for index in range(i - period, i):
            if current_hold == '':
                df['total_asset'][index] = current_cash
            elif current_hold == 'sz_50':
                df['total_asset'][index] = current_cash + current_etf_num * df['close_50'][i] * current_etf_num
            elif current_hold == 'hs_300':
                df['total_asset'][index] = current_cash + current_etf_num * df['close_300'][i] * current_etf_num
            elif current_hold == 'zz_500':
                df['total_asset'][index] = current_cash + current_etf_num * df['close_500'][i] * current_etf_num
            elif current_hold == 'gz':
                df['total_asset'][index] = current_cash + current_etf_num * df['close_gz'][i] * current_etf_num

        # 判断是否换仓
        sz_50_increase = (df['close_50'][i] - df['close_50'][i - period]) / df['close_50'][i - period]
        hs_300_increase = (df['close_300'][i] - df['close_300'][i - period]) / df['close_300'][i - period]
        zz_500_increase = (df['close_500'][i] - df['close_500'][i - period]) / df['close_500'][i - period]

        if sz_50_increase > hs_300_increase and sz_50_increase > zz_500_increase and sz_50_increase > 0:
            if current_hold == 'sz_50':
                continue
            else:
                if current_hold == 'hs_300':
                    current_cash = current_cash + sale_stock(df['close_300'][i], current_etf_num)
                elif current_hold == 'zz_500':
                    current_cash = current_cash + sale_stock(df['close_500'][i], current_etf_num)
                elif current_hold == 'gz':
                    current_cash = current_cash + sale_stock(df['close_gz'][i], current_etf_num)

                current_cash, current_etf_num = buy_stock(current_cash, df['close_50'][i])
                current_hold = 'sz_50'
        elif hs_300_increase > sz_50_increase and hs_300_increase > zz_500_increase and hs_300_increase > 0:
            if current_hold == 'hs_300':
                continue
            else:
                if current_hold == 'sz_50':
                    current_cash = current_cash + sale_stock(df['close_50'][i], current_etf_num)
                elif current_hold == 'zz_500':
                    current_cash = current_cash + sale_stock(df['close_500'][i], current_etf_num)
                elif current_hold == 'gz':
                    current_cash = current_cash + sale_stock(df['close_gz'][i], current_etf_num)

                current_cash, current_etf_num = buy_stock(current_cash, df['close_300'][i])
                current_hold = 'hs_300'
        elif zz_500_increase > sz_50_increase and zz_500_increase > hs_300_increase and zz_500_increase > 0:
            if current_hold == 'zz_500':
                continue
            else:
                if current_hold == 'sz_50':
                    current_cash = current_cash + sale_stock(df['close_50'][i], current_etf_num)
                elif current_hold == 'hs_300':
                    current_cash = current_cash + sale_stock(df['close_300'][i], current_etf_num)
                elif current_hold == 'gz':
                    current_cash = current_cash + sale_stock(df['close_gz'][i], current_etf_num)

                current_cash, current_etf_num = buy_stock(current_cash, df['close_500'][i])
                current_hold = 'zz_500'
        else:
            if current_hold == 'gz':
                continue
            elif current_hold == 'sz_50':
                current_cash = current_cash + sale_stock(df['close_50'][i], current_etf_num)
            elif current_hold == 'hs_300':
                current_cash = current_cash + sale_stock(df['close_300'][i], current_etf_num)
            elif current_hold == 'zz_500':
                current_cash = current_cash + sale_stock(df['close_500'][i], current_etf_num)

            current_cash, current_etf_num = buy_stock(current_cash, df['close_gz'][i])
            current_hold = 'gz'

        # 计算剩下未满周期的总金额
        if (i + period) > df.index[-1]:
            for index in range(i, df.index[-1] + 1):
                if current_hold == 'sz_50':
                    df['total_asset'][index] = current_cash + current_etf_num * df['close_50'][index]
                elif current_hold == 'hs_300':
                    df['total_asset'][index] = current_cash + current_etf_num * df['close_300'][index]
                elif current_hold == 'zz_500':
                    df['total_asset'][index] = current_cash + current_etf_num * df['close_500'][index]
                elif current_hold == 'gz':
                    df['total_asset'][index] = current_cash + current_etf_num * df['close_gz'][index]
                else:
                    df['total_asset'][index] = current_cash

        i += period

    df = df.drop(range(period), axis=0).reset_index(drop=True)
    sharp_rate = calculate_sharp_rate(init_fund, df, 0.03)
    max_drawdown = calculate_max_drawdown(df)
    calculate_rate_of_return(init_fund, df)
    print('夏普率:', sharp_rate)
    print('最大回撤:', max_drawdown)
    print('收益率:', df['rate_of_return'])







