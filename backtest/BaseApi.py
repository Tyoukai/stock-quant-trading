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


# 获取场内ETF信息
# ak.get_etf_inside('510500', '20230818', '20230928')
def get_etf_inside(code, start_date, end_date):
    return ak.fund_etf_fund_info_em(code, start_date, end_date)


# stock_sh_a_spot_em 沪a 列表 stock_sz_a_spot_em 深a列表
def list_low_price_stock(num):
    """
    获取沪深低价股列表
    :param num:
    :return: 低价股股票代码
    """
    sh_stock_list = ak.stock_sh_a_spot_em()
    sz_stock_list = ak.stock_sz_a_spot_em()
    df = pd.DataFrame()
    df['code'] = sh_stock_list['代码']
    df['name'] = sh_stock_list['名称']
    df['latest_close'] = sh_stock_list['最新价']
    df1 = pd.DataFrame()
    df1['code'] = sh_stock_list['代码']
    df1['name'] = sh_stock_list['名称']
    df1['latest_close'] = sh_stock_list['最新价']

    df.append(df1, ignore_index=True)
    return df


if __name__ == '__main__':
    # print(get_etf_inside('510500', '20230818', '20230928'))
    # print(get_daily_stock('000001.SZ', '20230818', '20230928'))
    print(ak.stock_sh_a_spot_em())
