from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.datasets import make_regression
import numpy as np
import matplotlib.pyplot as plt

X, y = make_regression(n_samples=50, n_features=1, noise=40, random_state=88)
# 线性回归
lr = LinearRegression()
lr.fit(X, y)
print(lr.coef_, lr.intercept_)
X_new = np.linspace(-2, 2.5, 100)
y_new = lr.predict((X_new.reshape(-1, 1)))

# 岭回归
ridge = Ridge(alpha=50)
ridge.fit(X, y)
y_new2 = ridge.predict(X_new.reshape(-1, 1))

fig = plt.figure(1, (10, 8))
ax = fig.add_subplot(111)
ax.scatter(X, y, s=70, color='g')
ax.plot(X_new, y_new, 'r--', label='Linear')
ax.plot(X_new, y_new2, 'k--', label='Ridge')
ax.legend(loc=3)
plt.grid()
plt.show()
