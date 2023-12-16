from backtest.BaseApi import *
import pandas as pd


def init_strategy(start_date, end_date):
    hs_300_etf = get_etf_inside('510300', start_date, end_date)
    df = pd.DataFrame()
    df['date'] = hs_300_etf['净值日期']
    df['close'] = hs_300_etf['单位净值']
    pass


if __name__ == '__main__':
    pass