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
df = get_fundamentals(q, '2023-08-10')
df.columns = ['code', 'mcap', 'na', '1/DA ratio', 'net income', 'growth', 'RD']

df.index = df['code'].values
df = df.drop('code', axis=1)
X = df.drop('mcap', axis=1)
y = df['mcap']
X = X.fillna(0)
y = y.fillna(0)

lr = LinearRegression()
model = lr.fit(X, y)
predict = pd.DataFrame(model.predict(X), index=y.index, columns=['predict_mcap'])
diff = df['mcap'] - predict['predict_mcap']
diff = pd.DataFrame(diff, index=y.index, columns=['diff'])
diff = diff.sort_values(by='diff', ascending=True)

sell_or_buy_list = diff.iloc[:10, 0]

stock_in_hand_map = {
    '600010.XSHG': 1,
    '600028.XSHG': 2,
    '600030.XSHG': 3,
    '600031.XSHG': 4,
    '600036.XSHG': 5,
    '600048.XSHG': 6,
    '600050.XSHG': 7,
    '600089.XSHG': 8,
    '600104.XSHG': 9,
    '600111.XSHG': 10
}
# 如果持有的股票不在sell_or_buy_list中则卖出
for stock_in_hand in stock_in_hand_map.keys():
    if stock_in_hand not in sell_or_buy_list:
        # 卖光所有股票
        pass
        # order_target_value(stock_in_hand, 0)
cash_each = 0
num = 0
if len(stock_in_hand_map) < 10:
    # 将剩余现金平均买入股票
    # 例如持有8只股票，手上还剩下3万现金，则每只股票买 3 / (10 -8)
    num = 10 - len(stock_in_hand_map)
    cash_each = 10000 / num
if num > 0 and cash_each > 0:
    for stock in sell_or_buy_list.index:
        if num > 0:
            # order_target_value(stock, cash_each)
            num -= 1