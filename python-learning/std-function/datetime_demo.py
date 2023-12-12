import datetime
# str转datetime格式
t1 = datetime.datetime.strptime('2023-12-06', '%Y-%m-%d')
print(t1)

# 计算两个日期之间天数
t2 = datetime.datetime(2023, 12, 10)
interval = t2 - t1
print(interval.days)

t3 = datetime.date(2023, 12, 12)
t4 = datetime.date(2023, 12, 15)
print((t4 - t3).days)

print(isinstance(t1, datetime.datetime))
print(isinstance(t3, datetime.date))


