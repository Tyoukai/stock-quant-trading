import pandas as pd
import numpy as np

data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
df = pd.DataFrame(data, columns=['Site', 'Age'])
# df.loc['net4'] = ['Facebook', 15]
# df['calculate'] = np.where(df['Age'] > 12, 1, 0)
# df['diff'] = df['Age'].diff()
# print(df)
# print('根据行索引读取数据：\n')
# print(df.loc['net'])
# print('根据列读取数据：\n')
# print(df['Site'])
# print(df['Age'][0])
#
# print(df.loc['net1'][1])

# se = df['Site']
# print(se)
# print(se.reindex(se.index[::-1]))

# print(df.reindex(df.index[::-1]))

# se = pd.Series([1, 2, 3, 4])
# print(se.cumsum())

print(df)
df = df.assign(money=pd.Series([100, 200, 300], index=df.index))
print('===========================')
print(df)











