import datetime
from datetime import timedelta
from matplotlib.dates import drange
import pandas as pd


# 将时间戳转换成datetime对象
ts = 1688548167190
ts = ts / 1000
date = datetime.datetime.fromtimestamp(ts)
print(type(date))

# 将datetime对象转换成时间戳（秒级别时间戳）
date.timestamp()

# str转datetime格式
t1 = datetime.datetime.strptime('2023-12-06', '%Y-%m-%d')
print(t1)

# 将datetime格式转换成str
tt = datetime.datetime.strftime(date, '%Y-%m-%d %H')
print(tt)

# 计算两个日期之间天数
t2 = datetime.datetime(2023, 12, 10)
interval = t2 - t1
print(interval.days)

t3 = datetime.date(2023, 12, 12)
t4 = datetime.date(2023, 12, 15)
print((t4 - t3).days)

print(isinstance(t1, datetime.datetime))
print(isinstance(t3, datetime.date))

# current_time = datetime.datetime(2024, 7, 28, 21, 41)
# print(int(datetime.datetime.now().timestamp() * 1000))
# before_time = current_time - timedelta(hours=42)
# str_before_time = before_time.strftime('%Y-%m-%d %H')
# print(datetime.datetime.strptime(str_before_time, '%Y-%m-%d %H').timestamp())


# start_time = datetime.datetime.fromtimestamp(1728028800)
# end_time = datetime.datetime.fromtimestamp(1729756800)


