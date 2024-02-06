import pandas as pd
import tushare as ts
import akshare as ak


# 获取每日收盘价格
def get_daily_stock(code, start_date, end_date):
    ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
    pro = ts.pro_api()
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    df = df.reindex(df.index[::-1]).reset_index(drop=True)
    return df


def get_stock_code_by_tu():
    """
    通过tushare获取股票代码
    :return:
    """
    ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return data


def get_daily_stock_by_ak(code, start_date, end_date, adjust='hfq'):
    """
    通过ak库获取股票每日复权价格，默认后复权
    :param code: 股票代码
    :param start_date:
    :param end_date:
    :param adjust: qfq:前复权 hfq：后复权 "":不复权
    :return:
    """
    stock_zh_a_hist_df = ak.stock_zh_a_hist(code, 'daily', start_date, end_date, adjust)
    stock_zh_a_hist_df.rename(
        columns={'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low'},
        inplace=True
    )
    if {'成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'}.issubset(stock_zh_a_hist_df.columns):
        stock_zh_a_hist_df = stock_zh_a_hist_df.drop(['成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'], axis=1)
    return stock_zh_a_hist_df


def get_realtime_stock_by_ak(market):
    """
    获取沪深两市实时股票价格，默认返回所有
    :param market: sh，sz
    :return: code, close
    """
    if market == 'sh':
        stock_sh_a_spot_em_df = ak.stock_sh_a_spot_em()
        sh_stock = pd.DataFrame()
        sh_stock['code'] = stock_sh_a_spot_em_df['代码']
        sh_stock['close'] = stock_sh_a_spot_em_df['最新价']
        sh_stock = sh_stock.dropna(axis=0, how='any').reset_index(drop=True)
        return sh_stock
    elif market == 'sz':
        stock_sz_a_spot_em_df = ak.stock_sz_a_spot_em()
        sz_stock = pd.DataFrame()
        sz_stock['code'] = stock_sz_a_spot_em_df['代码']
        sz_stock['close'] = stock_sz_a_spot_em_df['最新价']
        sz_stock = sz_stock.dropna(axis=0, how='any').reset_index(drop=True)
        return sz_stock
    else:
        stock_sh_a_spot_em_df = ak.stock_sh_a_spot_em()
        stock_sz_a_spot_em_df = ak.stock_sz_a_spot_em()
        sh_stock = pd.DataFrame()
        sh_stock['code'] = stock_sh_a_spot_em_df['代码']
        sh_stock['close'] = stock_sz_a_spot_em_df['最新价']
        sz_stock = pd.DataFrame()
        sz_stock['code'] = stock_sz_a_spot_em_df['代码']
        sz_stock['close'] = stock_sz_a_spot_em_df['最新价']
        hs_stock = sh_stock._append(sz_stock, ignore_index=True)
        hs_stock = hs_stock.dropna(axis=0, how='any').reset_index(drop=True)
        return hs_stock


def get_stock_constituent_by_ak(symbol):
    """
    获取指数成本股列表
    :param symbol: 指数代码 000300:沪深300
    :return:
    """
    index_df = ak.index_stock_cons_weight_csindex(symbol)
    index_df.rename(
        columns={'成分券代码': 'code'},
        inplace=True
    )
    return index_df['code']


# 获取场内ETF信息
# ak.get_etf_inside('510500', '20230818', '20230928')
def get_etf_inside(code, start_date, end_date):
    return ak.fund_etf_fund_info_em(code, start_date, end_date)


# stock_sh_a_spot_em 沪a 列表 stock_sz_a_spot_em 深a列表
def list_stock_code_and_price_by_ak(num):
    """
    获取沪深股列表
    :param num:
    :return: 股票代码
    """
    sh_stock_list = ak.stock_sh_a_spot_em()
    sz_stock_list = ak.stock_sz_a_spot_em()
    df_sh = pd.DataFrame()
    df_sh['code'] = sh_stock_list['代码']
    df_sh['name'] = sh_stock_list['名称']
    df_sh['close'] = sh_stock_list['最新价']
    df_sz = pd.DataFrame()
    df_sz['code'] = sz_stock_list['代码']
    df_sz['name'] = sz_stock_list['名称']
    df_sz['close'] = sz_stock_list['最新价']

    df_total = df_sh._append(df_sz, ignore_index=True)

    if num is None:
        return df_total
    return df_total[:num]


if __name__ == '__main__':
    # print(get_etf_inside('510500', '20230818', '20230928'))
    # print(get_daily_stock('000001.SZ', '20230818', '20230928'))
    # print(ak.stock_sh_a_spot_em())
    print(get_daily_stock_by_ak('600009', '20240206', '20240206', 'qfq'))
    # print(get_realtime_stock_by_ak('all'))
