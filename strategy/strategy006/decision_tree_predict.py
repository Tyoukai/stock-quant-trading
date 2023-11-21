from jqdatasdk import *
from jqdatasdk.technical_analysis import *
import datetime

auth('15629032381', '%')
stocks = get_index_stocks('000300.XSHG', '2023-07-12')
q = query(valuation.code, valuation.market_cap,
          balance.total_current_assets-balance.total_assets,
          balance.total_liability-balance.total_assets,
          balance.total_liability/balance.equities_parent_company_owners,
          (balance.total_assets-balance.total_current_assets)/balance.total_assets,
          balance.equities_parent_company_owners/balance.total_assets,
          indicator.inc_total_revenue_year_on_year,
          valuation.turnover_ratio,
          valuation.pe_ratio,
          valuation.pb_ratio,
          valuation.ps_ratio,
          indicator.roa).filter(valuation.code.in_(stocks))
df = get_fundamentals(q, '2023-07-12')
df.columns = ['code', '市值', '净运营资本', '净债务',
              '产权比例', '非流动资产比率', '股东权益比率', '营收增长率',
              '换手率', 'PE', 'PB', 'PS', '总资产收益率']
# print(df)

df.index = df.code.values
del df['code']
today = datetime.date(2023, 7, 12)
delta50 = datetime.timedelta(days=50)
delta1 = datetime.timedelta(days=1)
delta2 = datetime.timedelta(days=2)
history = today - delta50
yesterday = today - delta1
two_days_ago = today - delta2

df['动量线'] = list(MTM(df.index, two_days_ago,
                        timeperiod=10, unit='1d',
                        include_now=True, fq_ref_date=None).values())
df['成交量'] = list(VOL(df.index, two_days_ago,
                        M1=10, unit='1d', include_now=True,
                        fq_ref_date=None)[0].values())
df['累计能量线'] = list(OBV(df.index, two_days_ago, timeperiod=10).values())
df['平均差'] = list(DMA(df.index, check_date=two_days_ago,
                        timeperiod=10)[0].values())

df.fillna(0, inplace=True)

print(df)

