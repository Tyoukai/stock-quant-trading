import cufflinks as cf
import finplot as fplt


df = cf.datagen.ohlc()
# qf = cf.QuantFig(df, title='First Quant Figure', legend='top', name='GS')
fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])
fplt.show()
