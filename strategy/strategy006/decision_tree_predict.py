import pandas as pd
from jqdatasdk import *
import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


auth('15629032381', 'zkw123ZKW%')
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
# df = df.fillna(0, inplace=True)

df.index = df.code.values
del df['code']
today = datetime.date(2023, 7, 12)
delta50 = datetime.timedelta(days=50)
delta1 = datetime.timedelta(days=1)
delta2 = datetime.timedelta(days=2)
history = today - delta50
yesterday = today - delta1
two_days_ago = today - delta2

df['close1'] = list(get_price(stocks, end_date=yesterday, count=1, fq='pre', panel=False)['close'])
df['close2'] = list(get_price(stocks, end_date=history, count=1, fq='pre', panel=False)['close'])
df['return'] = df['close1'] / df['close2'] - 1
df['signal'] = np.where(df['return'] < df['return'].mean(), 0, 1)
print(df)

X = df.drop(['close1', 'close2', 'return', 'signal'], axis=1)
y = df['signal']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = DecisionTreeClassifier(random_state=1000)
clf.fit(X_train, y_train)
print(clf.score(X_train, y_train), clf.score(X_test, y_test))

factor_weight = pd.DataFrame({
    'features': list(X.columns),
    'importance': clf.feature_importances_
})

print(factor_weight)




