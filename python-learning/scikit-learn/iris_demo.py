from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

iris = load_iris()
# print(iris.keys())
# print(iris.feature_names)
# print(iris.target)

# X (150, 4)
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y)

print(X_train.shape)

knn_clf = KNeighborsClassifier(n_neighbors=5)
knn_clf.fit(X_train, y_train)
print('训练集准确率:', knn_clf.score(X_train, y_train))
print('验证集准确率:', knn_clf.score(X_test, y_test))

