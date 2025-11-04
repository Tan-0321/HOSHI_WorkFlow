
set xl  'rad /rad_{sh}'
set yl  'normalized quantities'
set ytics nomirror
set yr [-0.1:1.2]
set xr [0:1.2]
set key l t

file_sedov='/Users/ktakahashi/Dropbox/program/sedov/sedov.dat'

plot \
file_d1                 u (@j_rad0):(@j_dens0) w l ls 1 ti 'dens/dens_{sh}',\
file_d1                 u (@j_rad0):(@j_pres0) w l ls 2 ti 'pres/pres_{sh}',\
file_d1                 u (@j_rad0):(@j_vel0 ) w l ls 3 ti 'vel /vel_{sh}',\
file_d1  eve dj::(dj-1) u (@j_rad0):(@j_dens0) w p ls 1 ti '',\
file_d1  eve dj::(dj-1) u (@j_rad0):(@j_pres0) w p ls 2 ti '',\
file_d1  eve dj::(dj-1) u (@j_rad0):(@j_vel0 ) w p ls 3 ti '',\
file_d2                 u (@j_rad0):(@j_dens0) w l ls 1 ti '',\
file_d2                 u (@j_rad0):(@j_pres0) w l ls 2 ti '',\
file_d2                 u (@j_rad0):(@j_vel0 ) w l ls 3 ti '',\
file_d2  eve dj::(dj-1) u (@j_rad0):(@j_dens0) w p ls 1 ti '',\
file_d2  eve dj::(dj-1) u (@j_rad0):(@j_pres0) w p ls 2 ti '',\
file_d2  eve dj::(dj-1) u (@j_rad0):(@j_vel0 ) w p ls 3 ti '',\
file_d3                 u (@j_rad0):(@j_dens0) w l ls 1 ti '',\
file_d3                 u (@j_rad0):(@j_pres0) w l ls 2 ti '',\
file_d3                 u (@j_rad0):(@j_vel0 ) w l ls 3 ti '',\
file_d3  eve dj::(dj-1) u (@j_rad0):(@j_dens0) w p ls 1 ti '',\
file_d3  eve dj::(dj-1) u (@j_rad0):(@j_pres0) w p ls 2 ti '',\
file_d3  eve dj::(dj-1) u (@j_rad0):(@j_vel0 ) w p ls 3 ti '',\
file_d4                 u (@j_rad0):(@j_dens0) w l ls 1 ti '',\
file_d4                 u (@j_rad0):(@j_pres0) w l ls 2 ti '',\
file_d4                 u (@j_rad0):(@j_vel0 ) w l ls 3 ti '',\
file_d4  eve dj::(dj-1) u (@j_rad0):(@j_dens0) w p ls 1 ti '',\
file_d4  eve dj::(dj-1) u (@j_rad0):(@j_pres0) w p ls 2 ti '',\
file_d4  eve dj::(dj-1) u (@j_rad0):(@j_vel0 ) w p ls 3 ti '',\
file_d5                 u (@j_rad0):(@j_dens0) w l ls 1 ti '',\
file_d5                 u (@j_rad0):(@j_pres0) w l ls 2 ti '',\
file_d5                 u (@j_rad0):(@j_vel0 ) w l ls 3 ti '',\
file_d5  eve dj::(dj-1) u (@j_rad0):(@j_dens0) w p ls 1 ti '',\
file_d5  eve dj::(dj-1) u (@j_rad0):(@j_pres0) w p ls 2 ti '',\
file_d5  eve dj::(dj-1) u (@j_rad0):(@j_vel0 ) w p ls 3 ti '',\
file_sedov u 2:5 w l ls 11 ti 'Sedov' ,\
file_sedov u 2:4 w l ls 12 ti '' ,\
file_sedov u 2:3 w l ls 13 ti '' 

unset key
unset xr
unset yr