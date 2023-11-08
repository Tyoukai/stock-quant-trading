import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import tushare as ts

ts.set_token('99c90b0a4e59eb836aebcfd89e6d0aa62b77212fabaa9c7a5c81e888')
pro = ts.pro_api()
df = pro.daily(ts_code='000001.SZ', start_date='20230101', end_date='20230928')
df = df.reindex(df.index[::-1])

calculate_df = df.loc[:, ['trade_date', 'open', 'high', 'low', 'close']]
calculate_df['open_close'] = calculate_df['open'] - calculate_df['close']
calculate_df['high_low'] = calculate_df['high'] - calculate_df['low']
calculate_df['target'] = np.where((calculate_df['close'].shift(-1) > calculate_df['close']), 1, 0)
calculate_df = calculate_df.dropna()

X = calculate_df[['open_close', 'high_low']]
y = calculate_df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
knn_stock = KNeighborsClassifier(n_neighbors=10)
knn_stock.fit(X_train, y_train)
print(knn_stock.score(X_train, y_train))
print(knn_stock.score(X_test, y_test))

new_df = calculate_df.iloc[-20:]
new_df['knn_predict_signal'] = knn_stock.predict(new_df[['open_close', 'high_low']])
new_df['signal'] = new_df['knn_predict_signal'].diff()
new_df = new_df.fillna(0)
new_df['stock_num'] = new_df['signal'].cumsum() * 1500
new_df['stock_value'] = new_df['stock_num'] * new_df['close']
yesterday_cash = 20000.0
init_cash = 20000.0
new_df['mid_value'] = new_df['signal'] * 1500 * new_df['close']
new_df['cash_in_hand'] = np.zeros((1, 20))[0]
for index in new_df.index:
    new_df.loc[index, 'cash_in_hand'] = yesterday_cash - new_df.loc[index, 'mid_value']
    yesterday_cash = new_df.loc[index, 'cash_in_hand']
new_df['total'] = new_df['cash_in_hand'] + new_df['stock_value']
new_df['knn_yield'] = ((new_df['total'] - init_cash) / init_cash) * 100

fig = plt.figure(1, (10, 8))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.plot(new_df['trade_date'], new_df['knn_yield'], 'r--', label='yield')
ax1.plot(new_df['trade_date'], np.zeros((1, 20))[0], 'g--')
ax1.set_xticks(['20230901', '20230908', '20230915', '20230922', '20230928'])
ax1.legend(loc=3)

ax2.plot(new_df['trade_date'], new_df['total'], 'r--', label='total')
ax2.plot(new_df['trade_date'], np.ones((1, 20))[0] * 20000, 'g--')
ax2.set_xticks(['20230901', '20230908', '20230915', '20230922', '20230928'])
ax2.legend(loc=3)

plt.show()




