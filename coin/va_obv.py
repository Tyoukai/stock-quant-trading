import pandas as pd
from base_api import get_k_line_with_start_time
from base_api import draw_one_day_with_mpl
import mplfinance as mpl


def calculate_va_obv(local_df):
    local_df['va'] = (((local_df['close'] - local_df['low']) - (local_df['high'] - local_df['close']))
                      / (local_df['high'] - local_df['low']) * local_df['volume'])
    local_df['va'] = local_df['va'].cumsum()
    return local_df


def draw(local_df, local_symbol):
    local_df.index = pd.DatetimeIndex(local_df['start_time_format'])
    add_plot = [
        mpl.make_addplot(local_df['va'], type='line', color='r', label='va_obv', panel=2)
    ]
    draw_one_day_with_mpl(local_df, add_plot, local_symbol, (13), (1, 0.4, 0.4), True)


if __name__ == '__main__':
    symbols = ['SUIUSDT']
    # symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
    #            'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT',
    #            'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
    #            'FETUSDT', 'FILUSDT']

    start_time = 1714838400000
    for symbol in symbols:
        # 1、获取指定的k线信息
        result, one_day_df = get_k_line_with_start_time(symbol, start_time, '1d')
        if not result:
            continue
        # 2、计算va_obv
        calculated_one_day_df = calculate_va_obv(one_day_df)
        # 3、绘制图形
        draw(calculated_one_day_df, symbol)
