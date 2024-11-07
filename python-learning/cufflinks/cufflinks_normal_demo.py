import cufflinks as cf
import plotly
import numpy as np

df = cf.datagen.ohlc()
df['volume'] = np.ones(len(df.index))
setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)
df.iplot(kind='candle', title='bar-chart', subplots=True, shape=[3, 1])

