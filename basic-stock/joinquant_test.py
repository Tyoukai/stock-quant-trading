from jqdatasdk import *

# 登录聚宽的账号密码
auth('', '')
stocks = get_index_stocks('000016.XSHG', '2023-08-11')
q = query(valuation.code,
          # 市值
          valuation.market_cap,
          # 净资产 总资产 - 总负债
          balance.total_assets - balance.total_liability,
          # 资产负债率的倒数
          balance.total_assets / balance.total_liability,
          # 净利润
          income.net_profit,
          # 年度收入增长
          indicator.inc_revenue_year_on_year,
          # 研发费用
          balance.development_expenditure).filter(valuation.code.in_(stocks))
df = get_fundamentals(q, '2023-08-11')
df.columns = ['code', 'mcap', 'na', '1/DA ratio', 'net income', 'growth', 'RD']
print(df)


