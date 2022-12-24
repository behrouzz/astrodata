from datetime import datetime, timedelta
import numpy as np
import ephem
import pickle


def gmt_noon_exact(t):
    t = datetime(t.year, t.month, t.day, 12)
    o = ephem.Observer()
    o.long = '0'
    o.lat = '0'
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=ephem.date(t))
    noon = o.next_transit(sun, start=sunrise)
    return noon.datetime()


def get_coefs(year, deg=17):
    t0 = datetime(year, 1, 1, 12)
    tw = np.array([t0 + timedelta(days=i) for i in range(366)])
    t_ord = np.array([(i-datetime(year,1,1)).total_seconds() for i in tw])
    eot = np.array([(t-gmt_noon_exact(t)).total_seconds() for t in tw])
    coefs = np.polyfit(t_ord, eot, deg)
    return coefs


def create_dc(yr1=2020, yr2=2050, deg=17):
    years = np.arange(yr1, yr2+1)
    dc = {}
    for y in years:
        dc[y] = get_coefs(y, deg=deg)
    return dc

def save_coefs(yr1=2020, yr2=2050, deg=17, filename=None):
    if filename is None:
        filename = f'eot_{yr1}_{yr2}.pickle'
    dc = create_dc(yr1=2020, yr2=2050, deg=17)
    with open(filename, 'wb') as f:
        pickle.dump(dc, f)


def load_coefs_dc(file):
    with open(file, 'rb') as f:
        dc = pickle.load(f)
    return dc


def get_eot_from_coefs(t, coefs):
    f = np.poly1d(coefs)
    t_ord = (t-datetime(t.year,1,1)).total_seconds()    
    return f(t_ord)


def get_eot_from_dc(t, dc):
    coefs = dc[t.year]
    return get_eot_from_coefs(t, coefs)


"""
EXAMPLES
--------
t = datetime.utcnow()


dc = create_dc(yr1=2020, yr2=2050)
eot = get_eot_from_dc(t, dc)
print(eot)

# or:
coefs = get_coefs(2022)
eot = get_eot_from_coefs(t, coefs)
print(eot)

# or:
save_coefs()
dc = load_coefs_dc('eot_2020_2050.pickle')
eot = get_eot_from_dc(t, dc)
print(eot)
"""
