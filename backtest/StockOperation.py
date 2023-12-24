

def buy_stock(current_cash, price):
    """
    买指定股票熟料
    :param current_cash: 当前手持现金数量
    :param price: 当前股票的价格
    :return: 剩余现金数量，手持股票数量
    """
    stock_in_hand = current_cash // price
    left_cash = current_cash - price * stock_in_hand
    return left_cash, stock_in_hand


def sell_stock(price, stock_num):
    """
    卖股票
    :param price:
    :param stock_num:
    :return:
    """
    return price * stock_num

