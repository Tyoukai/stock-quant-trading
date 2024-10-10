import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

init = 1725954003000
x = []
y = np.linspace(50, 100, 3000)
for i in range(0, 3000):
    x.append(init + i)
date = pd.date_range(start='202409101230', periods=3000, freq='15min').strftime('%Y-%m-%d %H:%M').tolist()

fig = plt.figure(1, figsize=(6, 4))
ax = fig.add_subplot(111)
ax.plot(date, y, 'b-,', label='line')
ax.legend(loc=3)
# plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
# plt.gca().xaxis.set_major_locator()
ax.xaxis.set_major_locator(plt.MaxNLocator(4))
plt.show()
