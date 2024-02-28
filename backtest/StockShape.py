from sklearn.linear_model import LinearRegression
import numpy as np


def is_star(open, close, high, low):
    """
    十字星判断， 实体长度小于总长度的10%
    :param open:
    :param close:
    :param high:
    :param low:
    :return: True：是十字星， False：不是十字星
    """
    entity = abs(open - close)
    total = abs(high - low)
    if total == 0:
        return False
    return entity / total <= 0.1


def is_downtrend(stock, coef=-0.2, down_ratio=0.6):
    """
    判断当前股票是否是下跌趋势
    :param stock:
    :param coef: 当前股票的价格斜率，默认：-0.2
    :param down_ratio: 下跌天数所占比率，默认：0.6
    :return: 是否是下跌趋势，True：是下跌趋势， False：不是下跌趋势
    """
    if stock is None:
        return False
    total_count = len(stock.index)
    down_count = 0.0
    for i in range(total_count):
        open_price = stock['open'].iloc[i]
        close_price = stock['close'].iloc[i]
        if open_price > close_price:
            down_count += 1
    if down_count / total_count < down_ratio:
        return False

    x = np.arange(total_count).reshape(-1, 1)
    stock['mid_close'] = (stock['open'] + stock['close']) / 2.0
    lr = LinearRegression().fit(x, stock['mid_close'])
    if lr.coef_ <= coef:
        return True

    return False



