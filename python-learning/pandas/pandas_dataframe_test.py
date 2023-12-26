import pandas as pd
import numpy as np

df = pd.DataFrame()
series = pd.Series([1, 2, 3, 4, 5])
list = [5, 6, 7, 8, 9]
df['series'] = series
df['list'] = list
df['np'] = np.zeros(len(series))
print(df)

# 删除dataframe中的行
# df = df.drop(range(0, 2), axis=0)
# print(df)

# 相同列名不同dataframe合并
df1 = pd.DataFrame({
    'series': [6, 7, 8, 9],
    'list': [10, 11, 12, 13],
    'np': [0, 0, 0, 0]
})
df2 = df._append(df1, ignore_index=True)
df2.iloc[0] = [0, 0, 0]
print(df2)
