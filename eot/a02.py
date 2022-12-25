from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt

df = pd.read_csv('eot_2020_2050.csv')

x = df['time'].values
y = df['2020'].values

f = interpolate.interp1d(x, y)

xnew = x
ynew = f(x)

fig, ax = plt.subplots()
ax.scatter(x, y, s=1, c='b')
ax.scatter(xnew, ynew, s=1, c='r')
plt.show()
