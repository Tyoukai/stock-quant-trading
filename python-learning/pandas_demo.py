import pandas as pd

data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
df = pd.DataFrame(data, index=['net', 'net1', 'net2'], columns=['Site', 'Age'], dtype=str)
print(df)
print('根据行索引读取数据：\n')
print(df.loc['net'])
print('根据列读取数据：\n')
print(df['Site'])
print(df['Age'][0])

print(df.loc['net1'][1])
