import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=50, centers=2, random_state=6, cluster_std=1)
clf = svm.SVC(kernel='linear', C=1000)
clf.fit(X, y)

fig = plt.figure(1, (10, 8))
ax = fig.add_subplot(111)

ax.scatter(X[:, 0], X[:, 1], s=50, color='k')

gca = plt.gca()
xlim = gca.get_xlim()
ylim = gca.get_ylim()
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
XX, YY = np.meshgrid(xx, yy)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)
gca.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1],
            alpha=0.5, linestyles=['--', '-', '--'])
gca.scatter(clf.support_vectors_[:, 0],
            clf.support_vectors_[:, 1], s=100, linewidths=1)
plt.show()





