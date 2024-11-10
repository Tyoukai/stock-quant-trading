import numpy as np
import pandas as pd
import mplfinance as mpf
import cufflinks as cf

df = cf.datagen.ohlc()
df['volume'] = np.random.randint(low=1000, high=10000, size=len(df))

mpf.plot(df, type='candle', mav=(2, 5, 10), volume=True)
