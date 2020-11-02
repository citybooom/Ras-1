import numpy as np
# generate random data
N = 25
xp = [-5.0, 5.0]
x = np.random.uniform(xp[0],xp[1],(N,1))
e = 2*np.random.randn(N,1)
y = 2*x+e
w = np.ones(N)

# make the 3rd one outlier
y[2] += 30.0
w[2] = 100.0

from sklearn.linear_model import LinearRegression
# fit WLS using sample_weights
WLS = LinearRegression()

WLS.fit(x, y, sample_weight=w)

from matplotlib import pyplot as plt
plt.plot(x,y, '.')
print(WLS.coef_[0])
plt.plot(xp, xp*WLS.coef_[0])
plt.show()