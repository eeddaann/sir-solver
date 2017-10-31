import numpy as np
import matplotlib.pyplot as plt

vac_factor = 0.2
time = np.linspace(0,100,100)

s = np.random.poisson(5, 100)*time
i = np.random.poisson(5*vac_factor, 100)*time
r = np.random.poisson(5, 100)*time

total = s+i+r
s = s/total
i = i/total
r = r/total

print(s)
print(i)
print(r)
print(s+i+r)
plt.plot(s)
plt.plot(i)
plt.plot(r)
plt.show()