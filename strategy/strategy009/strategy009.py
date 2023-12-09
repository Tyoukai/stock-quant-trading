from backtest.BaseApi import get_etf_inside
from backtest.IndexCalculation import *
import pandas as pd

def init_strategy():
    """
    初始化策略
    :return:
    """
    # 上证50ETF 510050  start 2013-02-22
    # 沪深300ETF 510300 start 2012-05-11
    # 中证500ETF 510500 start 2013-02-22
    # 国债指数ETF 511010 start 2013-03-08

    sz_50_etf = get_etf_inside('510050', '20130308', '20231208')
    hs_300_etf = get_etf_inside('510300', '20130308', '20231208')
    zz_500_etf = get_etf_inside('510500', '20130308', '20231208')
    gz_etf = get_etf_inside('511010', '20130308', '20231208')
    sz_50_etf = sz_50_etf.reindex(sz_50_etf.index[::-1]).reset_index(drop=True)
    hs_300_etf = hs_300_etf.reindex(hs_300_etf.index[::-1]).reset_index(drop=True)
    zz_500_etf = zz_500_etf.reindex(zz_500_etf.index[::-1]).reset_index(drop=True)
    gz_etf = gz_etf.reindex(gz_etf.index[::-1]).reset_index(drop=True)

    df = pd.DataFrame()
    df['date'] = sz_50_etf['净值日期']
    df['close_50'] = sz_50_etf['单位净值']
    df['close_300'] = hs_300_etf['单位净值']
    df['close_500'] = zz_500_etf['单位净值']
    df['close_gz'] = gz_etf['单位净值']
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
    i = 20
    while i < df.index[-1]:
        sz_50_increase = (df['close_50'][i] - df['close_50'][i - 20]) / df['close_50'][i - 20]
        hs_300_increase = (df['close_300'][i] - df['close_300'][i - 20]) / df['close_300'][i - 20]
        zz_500_increase = (df['close_500'][i] - df['close_500'][i - 20]) / df['close_500'][i - 20]

        if sz_50_increase > hs_300_increase and sz_50_increase > zz_500_increase and sz_50_increase > 0:
            if current_hold == 'sz_50':
                continue
            else:
                if current_hold != '':
                    pass
                current_hold = 'sz_50'













