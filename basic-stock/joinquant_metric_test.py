from jqdatasdk import *
from jqdatasdk.technical_analysis import *

# 登录聚宽的账号密码
auth('15629032381', 't%')
security_list2 = ['000001.XSHE', '000002.XSHE', '601211.XSHG', '603177.XSHG']
MTM2 = MTM(security_list2,check_date='2023-07-12', timeperiod=12)
print(MTM2)

