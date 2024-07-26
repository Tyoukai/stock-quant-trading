from binance.spot import Spot


# https://api.binance.com
# https://api-gcp.binance.com
# https://api1.binance.com 可能会提供更好的性能
# https://api2.binance.com 可能会提供更好的性能
# https://api3.binance.com 可能会提供更好的性能
# https://api4.binance.com 可能会提供更好的性能
client = Spot(base_url='https://api4.binance.com')

# ping服务器
print(client.ping())

# 获取k线信息
# 北京时间CST，  标准时间UTC
# s -> 秒; m -> 分钟; h -> 小时; d -> 天; w -> 周; M -> 月
# 1s 1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M
kline = client.klines(symbol='BTCUSDT', interval='1m')

