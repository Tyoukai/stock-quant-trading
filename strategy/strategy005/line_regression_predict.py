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


df.index = df['code'].values
df = df.drop('code', axis=1)
X = df.drop('mcap', axis=1)
y = df['mcap']
X = X.fillna(0)
y = y.fillna(0)

lr = LinearRegression().fit(X, y)
# predict = pd.DataFrame(lr.predict(X), index=y.index, columns=['predict_mcap'])
# diff = df['mcap'] - predict['predict_mcap']
# diff = pd.DataFrame(diff, index=y.index, columns=['diff'])
# diff = diff.sort_values(by='diff', ascending=True)
#
# sell_or_buy_list = diff.iloc[:10, 0]

# 获取当前持有的股票
# hold_list = list(context.portfolio.positions.keys())
# # 如果持有的股票不在sell_or_buy_list中则卖出
#
# for stock_in_hand in hold_list:
#     if stock_in_hand not in sell_or_buy_list:
#         stock_sell = stock_in_hand
#         # 卖光所有股票
#         order_target_value(stock_sell, 0)
#
# # 判断当前股票数量是否小于股票上线
# cash = 0
# num = 0
# if len(context.portfolio.positions) < g.stocknum:
#     # 将剩余现金平均买入股票
#     # 例如持有8只股票，手上还剩下3万现金，则每只股票买 3 / (10 -8)
#     num = g.stocknum - len(context.portfolio.positions)
#     cash = context.portfolio.cash / num
# if num > 0:
#     for stock in sell_or_buy_list:
#         if stock in hold_list:
#             pass
#         else:
#             stock_bug = stock
#             order_target_value(stock_bug, cash)
#             num -= 1
# g.days += 1



