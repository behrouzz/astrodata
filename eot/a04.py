from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import ephem


def exact_noon(t, lon, lat):
    t = datetime(t.year, t.month, t.day, 12) + timedelta(hours=(lon/15))
    o = ephem.Observer()
    o.long = str(lon)
    o.lat = str(lat)
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=ephem.date(t))
    noon = o.next_transit(sun, start=sunrise)
    return noon.datetime()


def tim2ord(t):
    x = (t - datetime(t.year,1,1)).total_seconds()
    return x


df = pd.read_csv('eot_2020_2050.csv')

x = df['time'].values
y = df['2022'].values

f = interpolate.interp1d(x, y)

for i in range(1,13):
    print(i)
    t = datetime(2022, i, 15)
    #lon, lat = (7.4, 48)
    lon, lat = (0, 0)

    n1 = exact_noon(t, lon, lat)
    print(n1)

    t12 = datetime(t.year, t.month, t.day, 12) + timedelta(hours=(lon/15))

    eot = f(tim2ord(t))
    eot = np.array([eot])[0]

    eot = timedelta(seconds=eot)
    n2 = t12 - eot
    """
    if eot<0:
        eot = timedelta(seconds=-eot)
        n2 = t12 + eot
    else:
        eot = timedelta(seconds=eot)
        n2 = t12 - eot
    """
    print(n2)
    print(eot)
    print(eot.total_seconds())
    print('-'*50)
