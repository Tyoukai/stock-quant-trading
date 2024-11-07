import cufflinks as cf
import plotly

df = cf.datagen.ohlc()
qf = cf.QuantFig(df, title='First Quant Figure', legend='top', name='GS')
setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)
qf.add_bollinger_bands()
qf.iplot()

