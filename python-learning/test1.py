import time
import datetime

a = 172325340300
c = datetime.datetime.utcfromtimestamp(a).strftime('%d.%m.%Y %H:%M:%S')
print(type(c))
print(c)
b = time.localtime(a).strftime("%d.%m.%Y %H:%M:%S")
print(type(b))
print(b)
