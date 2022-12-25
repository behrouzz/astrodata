from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt

df = pd.read_csv('eot_2020_2050.csv')

x = df['time'].values[200:210]
y = df['2022'].values[200:210]

f = interpolate.interp1d(x, y)
ff = interpolate.interp1d(x, y, kind='cubic') #linear, quadratic, cubic


xnew = np.linspace(x[0], x[-1], 100)

plt.plot(x, y, 'o', xnew, f(xnew), '-')
plt.plot(x, y, 'o', xnew, ff(xnew), '-')
plt.show()
