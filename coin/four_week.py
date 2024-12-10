from base_api import get_latest_k_line
import datetime


def get_signal(local_df, local_symbol):
    current_close = local_df['close'].iloc[len(local_df.index) - 1]
    before_high = local_df['high'].iloc[0: len(local_df.index) - 1]
    before_low = local_df['low'].iloc[0: len(local_df.index) - 1]
    if current_close >= before_high.max():
        print(local_symbol + '做多，当前价格：' + current_close + '，之前最高价：' + before_high.max())
        return
    if current_close <= before_low.min():
        print(local_symbol + '做空，当前价格：' + current_close + '，之前最低价：' + before_high.min())
        return
    print(local_symbol + '观望')


if __name__ == '__main__':
    """
    四周交易法则：当前价格超过4周内最高价时，建立多头头寸，平仓空头，当价格跌破4周内最低价时，建立空头头寸，平仓多头。
    当然可以根据交易品种进行自定义，不一定是四周
    """
    # symbols = ['BTCUSDT']
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'TONUSDT', 'DOGEUSDT', 'ADAUSDT',
               'AVAXUSDT', 'SHIBUSDT', 'DOTUSDT', 'BCHUSDT', 'LINKUSDT', 'LTCUSDT', 'NEARUSDT',
               'UNIUSDT', 'PEPEUSDT', 'ICPUSDT', 'APTUSDT', 'WBETHUSDT', 'ETCUSDT', 'SUIUSDT', 'STXUSDT',
               'FETUSDT', 'FILUSDT']
    end_time = int(datetime.datetime.now().timestamp() * 1000)
    for symbol in symbols:
        # 1、获取指定周期的k线
        result, one_day_df = get_latest_k_line(symbol, '1d', 29, end_time)
        if not result:
            continue
        # 2、信号判断，判断做多还是做空，还是不做
        get_signal(one_day_df, symbol)
