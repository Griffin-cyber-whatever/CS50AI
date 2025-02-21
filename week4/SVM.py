# an example about support vector machine(SVM): finding a hyperplane that maximizes the distance (margin) between the closest points of different classes
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

# Create synthetic data: two linearly separable classes
np.random.seed(0)
# Class 0: centered at (-2, -2)
X0 = np.random.randn(20, 2) - [2, 2]
# Class 1: centered at (2, 2)
X1 = np.random.randn(20, 2) + [2, 2]
X = np.vstack((X0, X1))
y = [0] * 20 + [1] * 20

# Create and train the SVM classifier with a linear kernel
clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X, y)

# Extract the coefficients and intercept of the separating hyperplane
w = clf.coef_[0]
intercept = clf.intercept_[0]
# The equation of the line is: w[0]*x + w[1]*y + intercept = 0
# Rearranged for y:
a = -w[0] / w[1]
xx = np.linspace(-5, 5)
yy = a * xx - intercept / w[1]

# Plot the dataset, decision boundary, and support vectors
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired, edgecolors='k')
plt.plot(xx, yy, 'k-', label='Decision Boundary')
plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
            s=100, facecolors='none', edgecolors='red', label='Support Vectors')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('SVM with Linear Kernel')
plt.legend()
plt.show()