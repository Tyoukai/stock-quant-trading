from jqdatasdk import *
from sklearn.linear_model import LinearRegression
import pandas as pd

auth('15629032381', '%')
stocks = get_index_stocks('000016.XSHG', '2023-08-10')
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
# print(df)

df.index = df['code'].values
df = df.drop('code', axis=1)
X = df.drop('mcap', axis=1)
y = df['mcap']
X = X.fillna(0)
y = y.fillna(0)

lr = LinearRegression().fit(X, y)

# df['real_mcap'] = lr.predict(X).reshape(-1, 1)
print(df['mcap'])
print(lr.predict(X).reshape(-1, 1))
