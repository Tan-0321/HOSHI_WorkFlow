import sys

import numpy as np
import tostable as mod_ts

nmodel = 11

### data for stable isotopes ###
nctl_st  = mod_ts.get_nctl_st()
nuc_A_st = mod_ts.get_nuc_A_st()
nuc_Z_st = mod_ts.get_nuc_Z_st()
name_st  = mod_ts.get_name_st()
nuc_Z_max= nuc_Z_st[nctl_st-1]
################################

### import mass & proton number ###
file_mass = open('/data/home/ktakahashi/HOSHI_210703/data/mass49J1.txt','r')

nctl = int(file_mass.readline().rstrip('\n'))
nuc_A=[]
nuc_Z=[]
nuc_N=[]
for row_no in range(1,nctl+1):
    line = file_mass.readline().rstrip('\n').split()
    nuc_A.append( int(line[3])+int(line[4]) )
    nuc_Z.append( int(line[3]) )
    nuc_N.append( int(line[4]) )
#    print (row_no, line, nctl)
nuc_A = np.array(nuc_A)
nuc_Z = np.array(nuc_Z)
#print(nuc_A)
#print(nuc_Z)
file_mass.close()
###################################

### import solar abundance ###
#print (nuc_Z_max)
file_solar = open('/data/home/ktakahashi/HOSHI_210703/data/solar/asplund/abundAG09.txt','r')
data_solar = file_solar.readlines()
lmax = len(data_solar)-1

abund_solar = np.zeros(nuc_Z_max+1) + 100.
for l in range(1,lmax+1):
    line = data_solar[l].rstrip('\n').split()
    zt   = int(line[0])
    abund_solar[zt] = float(line[2])-12.
name_solar = [0] * (nuc_Z_max+1)
for kst in range(0,nctl_st):
    name_solar[nuc_Z_st[kst]] = name_st[kst]
#for nZ in range(0,nuc_Z_max+1):
#    print (nZ, name_solar[nZ], abund_solar[nZ])
file_solar.close()
##############################

file_yield = 'yield.dat'
data_yield = np.loadtxt(file_yield)
data_yield = data_yield[:,8:8+nctl]

for nm in range(0,nmodel):
    dum    = data_yield[nm,:]

    # converting into stable isotopes
    dum_st = mod_ts.tostable(nctl, nuc_A, nuc_Z, dum)

    # integrate
    abund = np.zeros(nuc_Z_max+1) + 1e-50
    for kst in range(0,nctl_st):
        nZ = nuc_Z_st[kst]
        abund[nZ] += dum_st[kst]

    # take log10 values
    for nZ in range(0,nuc_Z_max+1):
        abund[nZ]  = np.log10( abund[nZ] )

    # normalize with H
    abund_H = abund[1]
    for nZ in range(0,nuc_Z_max+1):
        abund[nZ] -= abund_H

    # normalize with solar values
    for k in range(0,nuc_Z_max+1):
        abund[k] -= abund_solar[k]

    # normalize with 16O
    abund_O = abund[8]
    for k in range(0,nuc_Z_max+1):
        abund[k] -= abund_O

#    for k in range(0,nuc_Z_max+1):
#        print(k,abund[k])
#    sys.exit()

    # stacking
    if nm==0 :
        data_abund = abund
    else :
        data_abund = np.vstack( [data_abund,abund] )

#print (data_abund)


data_output= data_abund
for k in range(0,nuc_Z_max+1):
    print('%5i'   %int(k)         , end='')
    print('%5s'   %name_solar[k]  , end='')
    for nm in range(0,nmodel):
        print('%14.5e'%data_abund[nm,k], end='')
    print()


