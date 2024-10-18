import datetime

from binance.spot import Spot
import pandas as pd


# https://api.binance.com
# https://api-gcp.binance.com
# https://api1.binance.com 可能会提供更好的性能
# https://api2.binance.com 可能会提供更好的性能
# https://api3.binance.com 可能会提供更好的性能
# https://api4.binance.com 可能会提供更好的性能
client = Spot(base_url='https://api4.binance.com')

# ping服务器
# print(client.ping())

# 获取k线信息
# 北京时间CST，  标准时间UTC
# s -> 秒; m -> 分钟; h -> 小时; d -> 天; w -> 周; M -> 月
# 1s 1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M , '1721964984000', '1722051384000'
# [
#   [
#     1499040000000,      // k线开盘时间
#     "0.01634790",       // 开盘价
#     "0.80000000",       // 最高价
#     "0.01575800",       // 最低价
#     "0.01577100",       // 收盘价(当前K线未结束的即为最新价)
#     "148976.11427815",  // 成交量
#     1499644799999,      // k线收盘时间
#     "2434.19055334",    // 成交额
#     308,                // 成交笔数
#     "1756.87402397",    // 主动买入成交量
#     "28.46694368",      // 主动买入成交额
#     "17928899.62484339" // 请忽略该参数
#   ]
# ]
kline = client.klines(symbol='BTCUSDT', interval='1d', startTime=1729123200000, endTime=1729240751572, limit=50)
df = pd.DataFrame(kline)
print(kline)

