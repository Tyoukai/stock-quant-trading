from base_api import get_latest_k_line
from base_api import draw_one_day_with_mpl
from moving_average import ema
import datetime
import mplfinance as mpl
import pandas as pd


def calculate_perspective_index(local_df, cycle):
    # 1、计算指定周期ema
    local_df, ema_name = ema(local_df, cycle, 'close')
    # 2、计算透视指标值
    local_df['bull_power'] = local_df['high'] - local_df[ema_name]
    local_df['bear_power'] = local_df['low'] - local_df[ema_name]
    local_df = local_df.dropna(axis=0, how='any').reset_index(drop=True)
    return local_df


def draw(local_df, symbol):
    local_df.index = pd.DatetimeIndex(local_df['start_time_format'])
    add_plot = [
        mpl.make_addplot(local_df['bull_power'], type='bar', color='#00FF00', panel=1),
        mpl.make_addplot(local_df['bear_power'], type='bar', color='#FF3030', panel=2)
    ]
    draw_one_day_with_mpl(local_df, add_plot, symbol, (13), (1, 0.3, 0.3))


if __name__ == '__main__':
    """
    透视指标
    """
    # symbols = ['PEPEUSDT']
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
               'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT',
               'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
               'FETUSDT', 'FILUSDT']
    for symbol in symbols:
        # 1、获取制定的K线信息
        result, one_day_df = get_latest_k_line(symbol, '1d', 120, int(datetime.datetime.now().timestamp() * 1000))
        if not result:
            continue
        # 2、计算透视指标
        calculated_one_day_df = calculate_perspective_index(one_day_df, 13)
        # 3、绘制图形
        draw(calculated_one_day_df, symbol)

