import numpy as np

np.random.seed(42)

x_array = np.random.standard_t(df=5, size=1000)
eps_array = np.random.normal(size=1000)
Y = 3 * x_array + 5 + eps_array

X = np.hstack([
    np.ones((1000, 1)),
    x_array.reshape((-1, 1))
])

coefs = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
print(coefs)