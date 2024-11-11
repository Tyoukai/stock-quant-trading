import mplfinance as mpf
import cufflinks as cf
import numpy as np

# 1、基本用法
# df = cf.datagen.ohlc()
# df['volume'] = np.ones(len(df.index))
# mpf.plot(df, type='candle', mav=(5, 8, 13), volume=True)

# 2、在主图上增加其他折线图
# df = cf.datagen.ohlc()
# df['middle'] = (df['high'] + df['low']) / 2.0
# add_plot = mpf.make_addplot(data=df[['high', 'low']])
# mpf.plot(df, type='candle', addplot=add_plot)

# 3、在主图上添加其他形式的图
df = cf.datagen.ohlc()
list_a = []
list_b = []
for i in range(len(df['high'])):
    if i % 3 == 0:
        list_a.append(df['high'].iloc[i])
    else:
        list_a.append(np.nan)
    if i % 5 == 0:
        list_b.append(df['high'].iloc[i])
    else:
        list_b.append(np.nan)
add_plot = [
    mpf.make_addplot(list_a, scatter=True, markersize=200, marker='^', color='k'),
    mpf.make_addplot(list_b, scatter=True, markersize=200, marker='v', color='g'),
    mpf.make_addplot(df[['high', 'low']])]
mpf.plot(df, type='candle', addplot=add_plot)


