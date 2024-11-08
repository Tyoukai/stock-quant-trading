import cufflinks as cf
import pandas as pd
import plotly
import numpy as np

print(cf.__version__)
setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)

# 柱状图
# df = pd.DataFrame({'Category': ['A', 'B', 'C', 'D'], 'Value': [21, 32, 33, 20]})
# df.iplot(kind='bar', x='Category', y='Value', xTitle='种类', yTitle='数量', title='直方图')

# 新直方图 默认按照行维度进行分组
# df = pd.DataFrame(np.random.randn(100, 4), columns='A B C D'.split())
# local_df = df.head(10)
# print(local_df)
# local_df.iplot('bar')

# 折线图 横坐标默认是df的index
# df = pd.DataFrame(np.random.randn(100, 4), columns='A B C D'.split())
# df.iplot()

# 散点图
# df = pd.DataFrame(np.random.randn(100, 4), columns='A B C D'.split())
# df.iplot(kind='scatter', x='A', y='B', mode='markers', size=20)

# 直方图
# mm = np.random.randn(1000)
# print(mm)
# df = pd.DataFrame({'a': mm}, columns=['a'])
# df.iplot(kind='histogram')

# 同种类型子图
# df = cf.datagen.histogram(4)
# df.iplot(kind='histogram', subplots=True)

# 不同种类型子图



