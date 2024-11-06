import mplfinance as mpf
import cufflinks as cf
import numpy as np

df = cf.datagen.ohlc()
df['volume'] = np.ones(len(df.index))
mpf.plot(df,type='candle', mav=(5, 8, 13), volume=True)
