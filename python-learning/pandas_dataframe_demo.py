import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))
print(df)
# print(df['B'][1])
# print(df.iloc[1][2])

# 筛选出B列大于零0的行
df1 = df[df['B'] > 0]
print(df1)


# 筛选出B列中大于0的行，同时只显示B列的数据
df2 = df['B'][df['B'] > 0]
print(df2)

# 筛选出B列大于0，同时C列小于零的行
df3 = df[(df['B'] > 0) & (df['C'] < 0)]
print(df3)

# 筛选出B列大于0，同时C列小于零，但最终只显示A、D两列的数据
df4 = df[['A', 'D']][(df['B'] > 0) & (df['C'] < 0)]
# df4 = df[['A', 'D']][(df['B']>0)&(df['C']<0)]
print(df4)



