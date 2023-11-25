import pandas as pd

df = pd.DataFrame()
series = pd.Series([1, 2, 3, 4, 5])
list = [5, 6, 7, 8, 9]
df['series'] = series
df['list'] = list
print(df)

