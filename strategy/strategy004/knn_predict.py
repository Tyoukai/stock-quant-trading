import numpy as np
import pandas as pd
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
calculate_df['target'] = np.where((calculate_df['close'].shift(-1) > calculate_df['close']), 1, -1)
calculate_df = calculate_df.dropna()

X = calculate_df[['open_close', 'high_low']]
y = calculate_df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
knn_stock = KNeighborsClassifier(n_neighbors=95)
knn_stock.fit(X_train, y_train)
print(knn_stock.score(X_train, y_train))
print(knn_stock.score(X_test, y_test))

