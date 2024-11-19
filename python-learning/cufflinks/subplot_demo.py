import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import cufflinks as cf

# 生成模拟数据
# https://blog.csdn.net/wuwei_201/article/details/108018343
np.random.seed(42)
# df = pd.DataFrame({
#     'Date': pd.date_range(start='2020-01-01', periods=100, freq='D'),
#     'Open': np.random.uniform(100, 200, 100),
#     'High': np.random.uniform(100, 200, 100),
#     'Low': np.random.uniform(100, 200, 100),
#     'Close': np.random.uniform(100, 200, 100),
#     'Volume': np.random.randint(100, 500, 100)
# })

df = cf.datagen.ohlc()
df['volume'] = np.random.randint(100, 500, len(df.index))

# 将日期设置为索引
# df.set_index('date', inplace=True)

# 创建子图布局
fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                    specs=[[{'type': 'candlestick'}], [{'type': 'bar'}], [{'type': 'scatter'}], [{'type': 'candlestick'}]])


# 添加K线图
# fig.add_trace(go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'], name='K线图'), row=1, col=1)
fig.add_trace(go.Bar(x=df.index, y=df['volume'], name='成交量'), row=1, col=1)

# 添加成交量柱状图
fig.add_trace(go.Bar(x=df.index, y=df['volume'], name='成交量'), row=2, col=1)

# 计算移动平均线
df['MA20'] = df['close'].rolling(window=20).mean()

# 添加移动平均线图
fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], mode='lines', name='MA20'), row=3, col=1)



fig.add_trace(go.Bar(x=df.index, y=df['volume'], name='成交量'), row=4, col=1)


# 更新布局
fig.update_layout(title_text='多类型子图示例')

# 显示图表
fig.show()
