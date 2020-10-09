from sklearn.neighbors import KNeighborsClassifier
import numpy as np

X = np.genfromtxt('train', delimiter=',')[1:]

KN = KNeighborsClassifier(n_neighbors=5)
KN.fit(X[:, 1:], X[:, 0])

y = np.genfromtxt('flag', delimiter=',')[1:]

pred = KN.predict(y)

b = ''.join(map(str, pred.astype(int)))
key = ''.join([chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8)])
print(key)