from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

X, y = make_regression(n_samples=50, n_features=1, noise=40, random_state=88)

fig = plt.figure(1, (10, 8))
ax = fig.add_subplot(111)
ax.scatter(X, y, s=70, color='g')
plt.grid()
plt.show()
