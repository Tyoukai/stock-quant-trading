import pandas_datareader as web
import matplotlib.pyplot as plt

# print('current version:' + web.__version__)
# start_date = '2020-01-01'
# end_date = '2020-03-18'
# #stooq Tiingo IEX
# data = web.data.DataReader('601318.ss', 'IEX', start_date, end_date)
# data.head()
# print(data)


dji = web.DataReader('^DJI', 'stooq')
print(dji)



# hyundai = web.DataReader('005380', 'naver', start='2020-01-01', end='2021-01-01')
# print(hyundai)



