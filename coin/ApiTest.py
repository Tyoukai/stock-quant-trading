from binance.spot import Spot

client = Spot()

# 获取k线信息
# 北京时间CST，  标准时间UTC
kline = client.klines(symbol='BTCUSDT', interval='1m')

