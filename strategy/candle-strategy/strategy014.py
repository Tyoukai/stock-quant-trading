from backtest.BaseApi import *
from datetime import date
import time


def hit_feature(code, start_date):
    """
    是否符合锤子线和上吊线形态
    量化定义：下影线长度是实体的2倍以上
    实体是上影线的10倍以上
    :param code:
    :param start_date:
    :return:
    """
    try:
        stock = get_daily_stock_by_ak(code, start_date, start_date)
        time.sleep(0.005)
        if stock_df is None or len(stock_df.index) == 0:
            return False
        if 'open' not in stock or 'close' not in stock or 'high' not in stock or 'low' not in stock:
            return False
        open = stock['open'].iloc[0]
        close = stock['close'].iloc[0]
        high = stock['high'].iloc[0]
        low = stock['low'].iloc[0]

        if open is None or close is None or high is None or low is None:
            return False

        entity = 0.0
        up_shadow = 0.0
        down_shadow = 0.0
        # 当天下跌
        if open > close:
            entity = open - close
            up_shadow = high - open
            down_shadow = close - low
        elif open < close:
            entity = close - open
            up_shadow = high - close
            down_shadow = open - low
        if entity == 0:
            return False

        if entity * 2 <= down_shadow and entity * 0.1 >= up_shadow:
            print(code)
            return True
        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    stock_df = list_stock_code_and_price_by_ak(None)
    # 判断今天是否是锤子线或上吊线形态
    stock_df['hit_feature'] = stock_df.apply(lambda x: hit_feature(x['code']), axis=1)
    stock_df = stock_df[stock_df['hit_feature']]
    print(stock_df)


