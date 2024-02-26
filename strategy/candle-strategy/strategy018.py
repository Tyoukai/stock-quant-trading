import numpy as np
import time
from sklearn.linear_model import LinearRegression
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
        # 判断两天的颜色是否相同
        if today_open >= today_close or yesterday_open >= yesterday_close:
            return False
        if today_open <= today_close or yesterday_open <= yesterday_close:
            return False
        # 判断今天实体是否在昨天实体中间
        if yesterday_open > today_open > yesterday_close and yesterday_open > today_close > yesterday_close:
            if is_star(today_open, today_close, today_high, today_low):
                x = np.arange(len(stock.index)).reshape(-1, 1)
                stock['mid_close'] = (stock['open'] + stock['close']) / 2.0
                lr = LinearRegression().fit(x, stock['mid_close'])
                if lr.coef_ <= -0.2:
                    print(code)
                    return True
                else:
                    return False

        else:
            return False
    except Exception as e:
        return False


if __name__ == '__main__':
    stock_df = list_stock_code_and_price_by_ak(None)
    stock_df['star_signal'] = stock_df.apply(lambda x: hit_feature(x['code'], '20240219', '20240226'), axis=1)
    stock_df = stock_df[stock_df['star_signal']]
    print(stock_df)