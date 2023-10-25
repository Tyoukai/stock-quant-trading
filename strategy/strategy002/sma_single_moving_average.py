import numpy as np
import matplotlib.pyplot as plt
from ..baseApi import tushare_api

df = tushare_api.get_daily_stock('000001.SZ', '20230901', '20230930')

