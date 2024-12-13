import mplfinance as mpl
from base_api import get_latest_k_line
import datetime
import pandas as pd


def draw(local_symbol, local_df):
    if local_symbol == 'BTCUSDT':
        mpl.plot(local_df, type='pnf', pnf_params=dict(box_size=1000, reversal=3))
        return
    if local_symbol == 'SOLUSDT':
        mpl.plot(local_df, type='pnf', pnf_params=dict(box_size=3, reversal=3))


if __name__ == '__main__':
    symbols = ['SOLUSDT']
    for symbol in symbols:
        # 获取k线信息
        result, one_day_df = get_latest_k_line(symbol, '1d', 120,
                                               int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 绘制点数图
        one_day_df.index = pd.DatetimeIndex(one_day_df['start_time_format'])
        draw(symbol, one_day_df)
        # mpl.plot(one_day_df, type='pnf', pnf_params=dict(box_size=1000, reversal=3))
