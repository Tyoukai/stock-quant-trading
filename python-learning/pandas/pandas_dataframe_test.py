import pandas as pd
import numpy as np

df = pd.DataFrame()
series = pd.Series([1, 2, 3, 4, 5])
list = [5, 6, 7, 8, 9]
df['series'] = series
df['list'] = list
df['np'] = np.zeros(len(series))
print(df)

df = df.drop(range(0, 2), axis=0)
print(df)

