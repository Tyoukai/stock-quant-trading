import datetime

from base_api import get_latest_k_line
from moving_average import ema


if __name__ == '__main__':
    """
    价格通道，根据价格通道寻找合适的入手点
    上轨线 = EMA + EMA * 轨道系数
    下轨线 = EMA - EMA * 轨道系数
    一般要求，将近期价格点位的95%包含在轨道内部，即两倍标准差
    """
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
               'WBTCUSDT', 'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'MATICUSDT',
               'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
               'FETUSDT', 'FILUSDT']
    for symbol in symbols:
        fifteen_minute_df = get_latest_k_line(symbol, '15m', 66, datetime.datetime.now().timestamp())
        ema_fifteen_minute_df = ema(fifteen_minute_df, 6, 'close')
        # 根据ema计算价格通道，找出符合条件的轨道系数




    pass