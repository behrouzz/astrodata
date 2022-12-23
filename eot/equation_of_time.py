from datetime import datetime, timedelta
import numpy as np
import ephem
import pickle



def get_noon_exact(t, lon, lat):    
    o = ephem.Observer()
    o.lat, o.long = str(lat), str(lon)
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=ephem.date(t))
    noon = o.next_transit(sun, start=sunrise)
    return noon.datetime()


def eot_exact(year):
    obs_loc = (0, 0, 0)
    lon, lat, h = obs_loc
    t0 = datetime(year, 1, 1, 12)
    tw = [t0 + timedelta(days=i) for i in range(365)]
    equ_time = []
    for t in tw:
        eq = t - get_noon_exact(t, lon, lat)
        equ_time.append(eq.total_seconds()/60)
    return np.array(tw), np.array(equ_time)

 

def get_eot_coefs(year, deg=17):
    tw, eq = eot_exact(year)
    x = np.arange(365)
    coefs = np.polyfit(x, eq, deg)
    return coefs



def save_eot_coefs(yr1=2020, yr2=2050, deg=17, filename='equation_of_time.pickle'):
    years = np.arange(yr1, yr2+1)
    eot_cfs_dic = {}
    for i in range(len(years)):
        eot_cfs_dic[years[i]] = get_eot_coefs(years[i], deg=deg)
    with open(filename, 'wb') as f:
        pickle.dump(eot_cfs_dic, f)

    

def get_eot(t, eot_cfs_dic):
    day = (t - datetime(t.year, 1, 1)).days
    coefs =  eot_cfs_dic[t.year]
    f = np.poly1d(coefs)
    return f(day)



# calculate and save the coefficients
save_eot_coefs(yr1=2020, yr2=2050, deg=17, filename='equation_of_time.pickle')


# using the saved coefficients
with open('equation_of_time.pickle', 'rb') as f:
    eot_cfs_dic = pickle.load(f)
    
t = datetime(2023, 1, 5, 12)

eot = get_eot(t, eot_cfs_dic)
print(eot)
