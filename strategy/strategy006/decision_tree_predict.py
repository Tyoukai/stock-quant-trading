from jqdatasdk import *

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

print(df)
