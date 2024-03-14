import time
from backtest.BaseApi import *
from backtest.StockShape import *


def hit_feature(code, start_date, end_date):
    try:
        stock = get_daily_stock_by_ak(code, start_date, end_date)
        if np.any(stock.isnull()):
            return False
        time.sleep(0.005)

        today_open = stock['open'].iloc[len(stock.index) - 1]
        today_low = stock['close'].iloc[len(stock.index) - 1]
        today_high = stock['high'].iloc[len(stock.index) - 1]
        today_close = stock['close'].iloc[len(stock.index) - 1]
        yesterday_open = stock['open'].iloc[len(stock.index) - 2]
        yesterday_close = stock['close'].iloc[len(stock.index) - 2]

        if yesterday_open <= yesterday_close:
            return False
        if today_open > today_close:
            return False

        # 判断今天实体是否在昨天实体中间
        if yesterday_open > today_open > yesterday_close and yesterday_open > today_close > yesterday_close:
            stock = stock.drop(len(stock.index) - 1, axis=0)
            if is_star(today_open, today_close, today_high, today_low) and is_downtrend(stock):
                print(code)
                return True
        else:
            return False
    except Exception as e:
        return False


if __name__ == '__main__':
    """
    获取沪深两市每日十字孕线形态
    """
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['star_signal'] = stock_df.apply(lambda x: hit_feature(x['code'], '20240306', '20240313'), axis=1)
    stock_df = stock_df[stock_df['star_signal']]
    print(stock_df)
