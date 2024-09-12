import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

x = np.linspace(0, 20, 3)
y = np.linspace(50, 100, 3)

fig = plt.figure(1, figsize=(6, 4))
ax = fig.add_subplot(111)
ax.plot(x, y, 'b-,', label='line')
ax.legend(loc=3)
# plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
plt.show()
