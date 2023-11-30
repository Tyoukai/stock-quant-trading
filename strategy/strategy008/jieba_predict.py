from jqdatasdk import *

auth('15629032381', '%')
df = finance.run_query(query(finance.CCTV_NEWS).filter(finance.CCTV_NEWS.day=='2023-08-19').limit(10))
print(df)
