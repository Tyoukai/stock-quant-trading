import numpy as np
import pandas as pd

list_a = [1, 2, 3]
s = pd.Series(list_a)
print(s.sum())
print(s.mean())
print(s.dtype)
print(s.cumsum())
