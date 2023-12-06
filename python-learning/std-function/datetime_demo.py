from datetime import datetime
# str转datetime格式
t1 = datetime.strptime('2023-12-06', '%Y-%m-%d')
print(t1)

# 计算两个日期之间天数
t2 = datetime(2023, 12, 10)
interval = t2 - t1
print(interval.days)

