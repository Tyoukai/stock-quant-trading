import numpy as np
from binance.spot import Spot
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import DayLocator, drange
import mplfinance as mpl


def get_latest_k_line(symbol_local, interval_local, max_delta, end_time):
    """
    自定义获取指定时间段的K线
    :param symbol_local: 代币符号
    :param interval_local: 15m:15分钟，1h：1小时
    :param max_delta: 想要获取多少个interval_local时间维度的k线
    :param end_time:
    :return:
    """
    client = Spot(base_url='https://api4.binance.com')
    # 计算开始时间
    if interval_local == '15m':
        length = max_delta * 15
        one_minute_unit = 60 * 1000
        unit = 15 * 60 * 1000
        end_time = end_time - end_time % one_minute_unit
        start_time = end_time - end_time % unit - unit * max_delta
        one_minute_df = None
        for i in range(0, length // 1000 + 1):
            tmp_start_time = start_time + i * 1000 * one_minute_unit
            tmp_end_time = 0
            if i == length // 1000:
                tmp_end_time = end_time
            else:
                tmp_end_time = start_time + i * 1000 * one_minute_unit + 1000 * one_minute_unit
            k_line = None
            try:
                k_line = client.klines(symbol=symbol_local, interval='1m', startTime=tmp_start_time,
                                       endTime=tmp_end_time,
                                       limit=1000)
            except BaseException:
                return False, pd.DataFrame()
            one_shard_minute_df = pd.DataFrame(k_line, columns=['start_time', 'open', 'high', 'low', 'close', 'vol',
                                                                'end_time', 'amount', 'num', '1', '2', '3'])
            if one_minute_df is None:
                one_minute_df = one_shard_minute_df
            else:
                one_minute_df = one_minute_df._append(one_shard_minute_df)

        one_minute_df = one_minute_df.reset_index(drop=True)
        fifteen_minute_df = pd.DataFrame()
        fifteen_minute_df['start_time'] = np.zeros(max_delta + 1)
        fifteen_minute_df['start_time'] = fifteen_minute_df['start_time'].astype(int)
        fifteen_minute_df['close'] = np.zeros(max_delta + 1)
        fifteen_minute_df['low'] = np.zeros(max_delta + 1)
        fifteen_minute_df['high'] = np.zeros(max_delta + 1)
        for i in range(max_delta + 1):
            tmp_one_minute_df = pd.DataFrame()
            if i == max_delta:
                tmp_one_minute_df = one_minute_df.iloc[i * 15: len(one_minute_df.index)]
            else:
                tmp_one_minute_df = one_minute_df[i * 15: i * 15 + 15]
            tmp_one_minute_df_low = (tmp_one_minute_df[['low']].copy()).astype('float')
            tmp_one_minute_df_close = (tmp_one_minute_df[['close']].copy()).astype('float')
            tmp_one_minute_df_high = (tmp_one_minute_df[['high']].copy()).astype('float')
            min_low = tmp_one_minute_df_low['low'].min()
            close = tmp_one_minute_df_close['close'].iloc[len(tmp_one_minute_df.index) - 1]
            high = tmp_one_minute_df_high['high'].iloc[len(tmp_one_minute_df.index) - 1]
            start_time = tmp_one_minute_df['start_time'].iloc[0]
            fifteen_minute_df.loc[i, 'start_time'] = start_time
            fifteen_minute_df.loc[i, 'close'] = close
            fifteen_minute_df.loc[i, 'high'] = high
            fifteen_minute_df.loc[i, 'low'] = min_low
        return True, fifteen_minute_df
    if interval_local == '1d':
        start_time = end_time - max_delta * 24 * 3600 * 1000
        k_line = None
        try:
            k_line = client.klines(symbol=symbol_local, interval='1d', startTime=start_time, endTime=end_time,
                                   limit=1000)
        except BaseException:
            return False, pd.DataFrame()
        one_day_df = pd.DataFrame(k_line, columns=['start_time', 'open', 'high', 'low', 'close', 'volume', 'end_time',
                                                   'amount', 'num', '1', '2', '3'])
        one_day_df['open'] = one_day_df['open'].astype(float)
        one_day_df['high'] = one_day_df['high'].astype(float)
        one_day_df['low'] = one_day_df['low'].astype(float)
        one_day_df['close'] = one_day_df['close'].astype(float)
        one_day_df['volume'] = one_day_df['volume'].astype(float)
        one_day_df['amount'] = one_day_df['amount'].astype(float)
        one_day_df['num'] = one_day_df['num'].astype(float)

        one_day_df['start_time'] = one_day_df['start_time'] / 1000
        start_time = datetime.datetime.fromtimestamp(int(one_day_df['start_time'][0]))
        start_time_str = datetime.datetime.strftime(start_time, '%Y%m%d')
        dates_str_list = pd.date_range(start=start_time_str, periods=len(one_day_df.index), freq='1d').strftime(
            '%Y-%m-%d').tolist()
        one_day_df['start_time_format'] = dates_str_list

        return True, one_day_df
    if interval_local == '1w':
        start_time = end_time - max_delta * 7 * 24 * 3600 * 1000
        k_line = None
        try:
            k_line = client.klines(symbol=symbol_local, interval='1w', startTime=start_time, endTime=end_time,
                                   limit=1000)
        except BaseException:
            return False, pd.DataFrame()
        one_week_df = pd.DataFrame(k_line, columns=['start_time', 'open', 'high', 'low', 'close', 'volume', 'end_time',
                                                   'amount', 'num', '1', '2', '3'])
        one_week_df['open'] = one_week_df['open'].astype(float)
        one_week_df['high'] = one_week_df['high'].astype(float)
        one_week_df['low'] = one_week_df['low'].astype(float)
        one_week_df['close'] = one_week_df['close'].astype(float)
        one_week_df['volume'] = one_week_df['volume'].astype(float)
        one_week_df['amount'] = one_week_df['amount'].astype(float)
        one_week_df['num'] = one_week_df['num'].astype(float)

        one_week_df['start_time'] = one_week_df['start_time'] / 1000
        start_time = datetime.datetime.fromtimestamp(int(one_week_df['start_time'][0]))
        start_time_str = datetime.datetime.strftime(start_time, '%Y%m%d')
        dates_str_list = pd.date_range(start=start_time_str, periods=len(one_week_df.index), freq='1w').strftime(
            '%Y-%m-%d').tolist()
        one_week_df['start_time_format'] = dates_str_list
        return True, one_week_df
    return False, pd.DataFrame()


def draw_plot_day(df_local, according_to_columns, symbol):
    """
    绘制日级别的通用图形
    :param df_local: 计算好的df
    :param according_to_columns: 纵坐标list
    :param symbol: 对应的币种标识
    :return:
    """
    color_list = ['#000000', '#0000FF', '#A52A2A', '#808080', '#008000', '#00FF00', '#FFC0CB', '#FF0000', '#FFFF00']

    df_local['start_time'] = df_local['start_time'] / 1000
    start_time = datetime.datetime.fromtimestamp(int(df_local['start_time'][0]))
    start_time_str = datetime.datetime.strftime(start_time, '%Y%m%d')
    dates_str_list = pd.date_range(start=start_time_str, periods=len(df_local.index), freq='1d').strftime('%Y-%m-%d').tolist()
    dates = []
    for date_str_list in dates_str_list:
        dates.append(datetime.datetime.strptime(date_str_list, '%Y-%m-%d'))

    fig = plt.figure(1, figsize=(15, 7))
    ax = fig.add_subplot(111)
    index = 0
    for according_to_column in according_to_columns:
        ax.plot_date(dates, df_local[according_to_column], color_list[index], label=according_to_column)
        index += 1
    ax.legend(loc=3)
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.xaxis.set_minor_locator(DayLocator())
    plt.title(label=symbol)
    plt.xticks(rotation=30)
    plt.show()


def draw_one_day_with_mpl(local_df, add_plot, symbol, mav, panel_ratios):
    """
    通过mpl绘制k线图
    :param local_df:
    :param add_plot: 绘制图形的plot
    :param symbol: 符号
    :param mav: 所要显示的移动平均线周期，传入元组
    :param panel_ratios: 主图与附图的显示比例
    :return:
    """
    my_color = mpl.make_marketcolors(up='#00FF00', down='#FF3030', inherit=True, volume='inherit')
    my_style = mpl.make_mpf_style(marketcolors=my_color, gridaxis='both', gridstyle='-.', y_on_right=False)
    mpl.plot(local_df, type='candle', datetime_format='%Y-%m-%d', style=my_style, panel_ratios=panel_ratios,
             mav=mav, addplot=add_plot, title=symbol)

