import pandas as pd
import numpy as np

df = pd.DataFrame({
    '数学成绩': [90, 80, 70, 60],
    '语文成绩': [100, 90, 80, 70],
    '英语成绩': [110, 100, 90, 80]
})

# axis 0: 以列的维度进行运算
# df[['语文成绩', '英语成绩']] = df[['语文成绩', '英语成绩']].div(df['数学成绩'], axis=0)
# print(df)
#
# df = df.div([2, 3, 4], axis=1)
# print(df)
# df = df.sort_values(by=['数学成绩'], ascending=True)
# print(df)

print(df.drop(0, axis=0))




