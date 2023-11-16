from sklearn.datasets import make_regression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np

X, y = make_regression(n_samples=100,
                       n_features=1, noise=60, random_state=18)

reg = DecisionTreeRegressor(max_depth=None)
reg.fit(X, y)
X_new = np.linspace(-2.5, 3.5, 100)
y_new = reg.predict(X_new.reshape(-1, 1))

reg2 = RandomForestRegressor(n_estimators=100)
reg2.fit(X, y)
y_new_2 = reg2.predict(X_new.reshape(-1, 1))


fig = plt.figure(1, (10, 8))
ax = fig.add_subplot(111)
ax.scatter(X, y, s=100, color='k')
ax.plot(X_new, y_new, 'r--')
ax.plot(X_new, y_new_2, 'g-')
plt.grid()
plt.show()
