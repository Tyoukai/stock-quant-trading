import mplfinance as mpl
import cufflinks as cf


df = cf.datagen.ohlc()
# box_size: 每个方格的数值，每个 O 与 X 的点数高度。例如，如果您将方格值设为 10 点，且每一个 X 意味着上涨 10 点，则一列 6 个 X 代表着上涨 60 点。O 与之相反。
# reversal：转向距离，趋势即将发生逆转时，价格应该在相反方向经过的格数（以开始新的一列）。最常见的转向距离是 3
mpl.plot(df, type='pnf', pnf_params=dict(box_size=20, reversal=3))
print('close')
