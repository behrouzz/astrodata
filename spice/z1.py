from jplephem import spk

#fname = 'de440_2022_2025.bsp'
fname = 'de440s_2030.bsp'
#fname = 'jup380s_2225.bsp'

k = spk.SPK.open(fname)
#print(k)
print(k.comments())
k.close()
