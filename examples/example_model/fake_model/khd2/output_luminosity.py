import math
import sys

import numpy as np
import read_summary as rs
import read_writestr as rw

# constants
year = 365*24*3600.

# read summary data
summ = rs.Summary('../summary/summary.txt')
summ.read_file()

lmax = summ.get_lmax()
print(lmax)
with open("luminosity.dat","w") as file:
    for l in range(0,lmax):
        time = summ.get_time(l)
        rtime= summ.get_rtime(l)
        nstg = summ.get_nstg(l)

        temp_center = summ.get_tempc(l)
        dens_center = summ.get_densc(l)
        entr_center = summ.get_entrc(l)
        lnuc        = summ.get_lnuc(l)
        lneu        = summ.get_lneu(l)

#        str = rw.Structure('../writestr/',nstg)
#        str.read_file()
#        ndv = str.get_ndiv()
#        temp_center = str.get_temp(20)
#        dens_center = str.get_dens(20)
#        entr_center = str.get_entr(20)
#        lnuc= str.get_lum_nuc(ndv)
#        lneu= str.get_lum_neu(ndv)
        file.write("{:5d} {:.5e} {:.5e} {:.5e} {:.5e} {:.5e} {:.5e} \n"
                   .format(nstg,rtime
                           ,dens_center
                           ,temp_center
                           ,entr_center
                           ,lnuc
                           ,lneu))
    
