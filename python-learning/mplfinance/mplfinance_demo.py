import mplfinance as mpf
import cufflinks as cf
import numpy as np

# 1、基本用法
df = cf.datagen.ohlc()
df['volume'] = abs(df['low'] * 1000)
mpf.plot(df, type='candle', style='charles', mav=(5, 8, 13), volume=True)

# 2、在主图上增加其他折线图
# df = cf.datagen.ohlc()
# df['middle'] = (df['high'] + df['low']) / 2.0
# add_plot = mpf.make_addplot(data=df[['high', 'low']])
# mpf.plot(df, type='candle', addplot=add_plot)

# 3、在主图上添加其他形式的图
# df = cf.datagen.ohlc()
# df['volume'] = abs(df['low'] * 1000)
# list_a = []
# list_b = []
# for i in range(len(df['high'])):
#     if i % 3 == 0:
#         list_a.append(df['high'].iloc[i])
#     else:
#         list_a.append(np.nan)
#     if i % 5 == 0:
#         list_b.append(df['high'].iloc[i])
#     else:
#         list_b.append(np.nan)
# add_plot = [
#     mpf.make_addplot(list_a, scatter=True, markersize=200, marker='^', color='k'),
#     mpf.make_addplot(list_b, scatter=True, markersize=200, marker='v', color='g'),
#     mpf.make_addplot(df[['high', 'low']])]
# mpf.plot(df, type='candle', addplot=add_plot, volume=True)

# 4、设置蜡烛图的颜色及样式
# df = cf.datagen.ohlc()
# df['volume'] = abs(df['low'] * 1000)
# """
# make_marketcolors() 设置k线颜色
# :up 设置阳线柱填充颜色
# :down 设置阴线柱填充颜色
# ：edge 设置蜡烛线边缘颜色 'i' 代表继承k线的颜色
# ：wick 设置蜡烛上下影线的颜色
# ：volume 设置成交量颜色
# ：inherit 是否继承, 如果设置了继承inherit=True，那么edge即便设了颜色也会无效
# """
# my_color = mpf.make_marketcolors(up='#00FF00', down='#FF3030', inherit=True, volume='inherit')
# """
# make_mpf_style() 设置mpf样式
# ：gridaxis:设置网格线位置,both 水平+垂直, horizontal水平,vertical垂直
# ：gridstyle:设置网格线线型
# ：y_on_right:设置y轴位置是否在右
# """
# my_style = mpf.make_mpf_style(marketcolors=my_color, gridaxis='horizontal', gridstyle='-.', y_on_right=False)
# """
# plot绘图的部分参数
# :type设置图像类型'ohlc'/'candle'/'line/renko'
# :mav 绘制平局线
# :show_nontrading= True 显示非交易日（k线之间有间隔）,False 不显示交易日，k线之间没有间隔
# :title:设置标题
# :ylabel=设置主图Y轴标题
# ：ylabel_lower 设置成交量一栏Y坐标标题
# :figratio:设置图形纵横比
# :figscale 设置图像的缩小或放大,1.5就是放大50%，最大不会超过电脑屏幕大小
# ：style 设置整个图表样式，可以使用前面设置的样式my_style,只能在plot函数中使用指定整个图表样式，不能在make_addplot中使用。
# savefig:导出图片，填写文件名及后缀
# """
# mpf.plot(df, type='candle', mav=(5, 8, 13), volume=True, style=my_style, title='title', ylabel_lower='volume')

# 5、设置子图
# df = cf.datagen.ohlc()
# df['volume'] = abs(df['low'] * 1000)
# df['middle'] = (df['low'] + df['high']) / 2.0
# df['up'] = df['high'] * 1.2
# df['down'] = df['low'] * 0.8
#
# addplot标签中label用来设置图例
# add_plot = [
#     mpf.make_addplot(df['up'], type='line', color='k', label='up'),
#     mpf.make_addplot(df['down'], type='line', color='r'),
#     mpf.make_addplot(df['volume'], type='bar', color='b', panel=1),
#     mpf.make_addplot(df['middle'], type='bar', color='k', panel=2)
# ]
#
# mpf.plot(df, type='candle', addplot=add_plot, datetime_format='%Y-%m-%d',
#          panel_ratios=(1, 0.3, 0.3))
