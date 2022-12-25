from datetime import datetime, timedelta
import numpy as np
import ephem
import pandas as pd


def gmt_noon_exact(t):
    t = datetime(t.year, t.month, t.day, 12)
    o = ephem.Observer()
    o.long = '0'
    o.lat = '0'
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=ephem.date(t))
    noon = o.next_transit(sun, start=sunrise)
    return noon.datetime()


def eot_table_year(year):
    t0 = datetime(year, 1, 1, 12)
    tw = np.array([t0 + timedelta(days=i) for i in range(365)])
    y = np.array([(t-gmt_noon_exact(t)).total_seconds() for t in tw])
    return y


def tim2ord(t):
    x = (t - datetime(t.year,1,1)).total_seconds()
    return x


def ord2tim(x, year):
    t0 = datetime(year, 1, 1)
    tim = t0 + timedelta(seconds=x)
    return tim


def eot_table(y1, y2):
    dc = {}
    for i in range(y1, y2+1):
        dc[str(i)] = eot_table_year(i)

    df = pd.DataFrame(dc)

    t0 = datetime(y1, 1, 1, 12)
    tw = np.array([t0 + timedelta(days=i) for i in range(365)])
    x = np.array([int(tim2ord(i)) for i in tw])

    df.index = x
    df.index.name = 'time'
    return df



if __name__ == "__main__":
    df = eot_table(2020, 2050)
    df.to_csv('eot_2020_2050.csv')
