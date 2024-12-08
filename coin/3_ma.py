import pandas as pd
from base_api import get_latest_k_line
from base_api import draw_one_day_with_mpl
import datetime
from moving_average import ema
import mplfinance as mpl


def draw(local_df, local_symbol):
    local_df.index = pd.DatetimeIndex(local_df['start_time_format'])
    add_plot = [
        mpl.make_addplot(local_df[ema_4_name], type='line', color='g', panel=1, label='ema4'),
        mpl.make_addplot(local_df[ema_9_name], type='line', color='k', panel=1, label='ema9'),
        mpl.make_addplot(local_df[ema_18_name], type='line', color='r', panel=1, label='ema18')
    ]
    draw_one_day_with_mpl(local_df, add_plot, local_symbol, (4, 9, 18), (1, 0.5), False)


if __name__ == '__main__':
    """
    期货技术分析-三线交易原则
    """
    # symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
    #            'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT',
    #            'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
    #            'FETUSDT', 'FILUSDT']
    symbols = ['PEPEUSDT']
    for symbol in symbols:
        # 获取指定的k线信息
        result, one_day_df = get_latest_k_line(symbol, '1d', 240, int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 计算不同维度的移动平均线
        one_day_df, ema_4_name = ema(one_day_df, 4, 'close')
        one_day_df, ema_9_name = ema(one_day_df, 9, 'close')
        one_day_df, ema_18_name = ema(one_day_df, 18, 'close')
        # 给出买入卖出信号
        # if ((one_day_df[ema_4_name].iloc[len(one_day_df.index)] > one_day_df[ema_9_name].iloc[len(one_day_df.index)])
        #         and (one_day_df[ema_4_name].iloc[len(one_day_df.index)] > one_day_df[ema_18_name].iloc[len(one_day_df.index)])):
        #     print('up notice')
        # if ((one_day_df[ema_4_name].iloc[len(one_day_df.index)] < one_day_df[ema_9_name].iloc[len(one_day_df.index)])
        #         and (one_day_df[ema_4_name].iloc[len(one_day_df.index)] < one_day_df[ema_18_name].iloc[len(one_day_df.index)])):
        #     print('down notice')
        # 画图
        draw(one_day_df, symbol)
