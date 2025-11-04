file_summary = '../summary/summary.txt'

nstg = file_w1[16:20]
title= 'nstg = '.nstg

set multiplot layout 3,3

set style line 10 ps 0.1 pt 1 lc 0 dt (7,10)

set style line 1 ps 0.1 pt 6 lc 1
set style line 2 ps 0.1 pt 6 lc 2
set style line 3 ps 0.1 pt 6 lc 3
set style line 4 ps 0.1 pt 6 lc 4
set style line 5 ps 0.1 pt 6 lc 5
set style line 6 ps 0.1 pt 6 lc rgb 'gold'
set style line 7 ps 0.1 pt 6 lc rgb 'forest-green'
set style line 8 ps 0.1 pt 6 lc rgb 'dark-gray'
set style line 9 ps 0.1 pt 6 lc rgb 'purple'

set style line 11 ps 0.1 pt 6 dt (2,3) lc 1
set style line 12 ps 0.1 pt 6 dt (2,3) lc 2
set style line 13 ps 0.1 pt 6 dt (2,3) lc 3
set style line 14 ps 0.1 pt 6 dt (2,3) lc 4
set style line 15 ps 0.1 pt 6 dt (2,3) lc 5
set style line 16 ps 0.1 pt 6 dt (2,3) lc rgb 'gold'
set style line 17 ps 0.1 pt 6 dt (2,3) lc rgb 'forest-green'
set style line 18 ps 0.1 pt 6 dt (2,3) lc rgb 'dark-gray'

###
load 'plot_settings.gp'
load 'plot_stats.gp'
###

###
#
set label 1 title at graph 0.06,0.92
set label 2 'time='.time.'s' at graph 0.06,0.82
set label 3 'dt  ='.dtime.'s' at graph 0.06,0.72
load 'plot_HR.gp'
unset label
#
#load 'plot_mr_d.gp'
#load 'plot_rad_epsnab.gp'
#load 'plot_rad_d.gp'

load 'plot_mr_omgxj.gp'
load 'plot_mr_mag.gp'
###

###
#load 'plot_rad_Ts.gp'
#load 'plot_rad_denspres.gp'
#load 'plot_rad_x.gp'

load 'plot_rhoctc.gp'
load 'plot_mr_d.gp'
load 'plot_mr_epsnab.gp'
###

###
load 'plot_mr_Ts.gp'
load 'plot_mr_denspres.gp'
load 'plot_mr_x.gp'
###


###
#load 'plot_total.gp'
#load 'plot_mr_omgxj.gp'
#load 'plot_mr_mag.gp'
###
#load 'plot_rotmag.gp'
#load 'plot_Rossby_Brad.gp'
#load 'plot_Teff_taucv.gp'
###

unset multiplot