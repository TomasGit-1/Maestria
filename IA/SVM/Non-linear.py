import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


xx, yy = np.meshgrid(np.linspace(-3, 3, 500), np.linspace(-3, 3, 500))
# np.random.seed(0)
# X = np.random.randn(300, 2)
# Y = np.logical_xor(X[:, 0] > 0, X[:, 1] > 0)

X, Y = make_circles(n_samples=1_000, factor=0.3, noise=0.05, random_state=0)
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
#{‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’}
clf = svm.NuSVC(gamma="auto", kernel="poly")
modeloGauss = clf.fit(X, Y)
y_pred = modeloGauss.predict(X_test)

# plot the decision function for each datapoint on the grid
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.imshow(
    Z,
    interpolation="nearest",
    extent=(xx.min(), xx.max(), yy.min(), yy.max()),
    aspect="auto",
    origin="lower",
    cmap=plt.cm.PuOr_r,
)
contours = plt.contour(xx, yy, Z, levels=[0], linewidths=2, linestyles="dashed")

plt.scatter(X[:, 0], X[:, 1], s=30, c=Y, cmap=plt.cm.Paired, edgecolors="k")
plt.scatter(X_test[:, 0], X_test[:, 1], s=30, c=y_pred, cmap=plt.cm.inferno, edgecolors="w")
plt.xticks(())
plt.yticks(())
plt.axis([-3, 3, -3, 3])
plt.show()
print("\n================================")