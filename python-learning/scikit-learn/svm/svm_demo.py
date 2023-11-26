import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=50, centers=2, random_state=6, cluster_std=1)
# clf = svm.SVC(kernel='linear', C=1000)
# clf.fit(X, y)

fig = plt.figure(1, (10, 8))
ax = fig.add_subplot(111)

ax.scatter(X[:, 0], X[:, 1], s=50, color='k')
print(plt.gca().get_xlim())
print(plt.gca().get_ylim())

plt.show()





