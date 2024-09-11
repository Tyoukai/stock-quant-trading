import time
import datetime

import numpy as np

import pandas as pd

map = {
    'start_time': [1557502800, 1559502800, 1567502800]
}
df = pd.DataFrame(map)
df['new'] = np.zeros(len(df))
df['new'] = df['new'].astype('str')
for i in range(len(df.index)):
    df.loc[i, 'new'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(df.loc[i, 'start_time']))

a = 1557502800
local_a = time.localtime(a)
print(local_a)
local_a_str = time.strftime("%Y-%m-%d %H:%M:%S", local_a)
print(local_a_str)
print(type(local_a_str))