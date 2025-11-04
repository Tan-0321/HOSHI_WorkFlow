set term pdf font ',12' size 5,5
set outp "plot_dynamic.pdf"

file_summary = '../summary/summary.txt'
iplot=6

if( iplot==1 ){
 file_d1 = '../writestr/dyn00002.txt'
 file_d2 = '../writestr/dyn00004.txt'
 file_d3 = '../writestr/dyn00006.txt'
 file_d4 = '../writestr/dyn00008.txt'
 file_d5 = '../writestr/dyn00010.txt'
}
if( iplot==2 ){
 file_d1 = '../writestr/dyn00060.txt'
 file_d2 = '../writestr/dyn00070.txt'
 file_d3 = '../writestr/dyn00080.txt'
 file_d4 = '../writestr/dyn00090.txt'
 file_d5 = '../writestr/dyn00100.txt'
}
if( iplot==3 ){
 file_d1 = '../writestr/dyn00180.txt'
 file_d2 = '../writestr/dyn00210.txt'
 file_d3 = '../writestr/dyn00240.txt'
 file_d4 = '../writestr/dyn00270.txt'
 file_d5 = '../writestr/dyn00300.txt'
}
if( iplot==4 ){
 file_d1 = '../writestr/dyn00600.txt'
 file_d2 = '../writestr/dyn00700.txt'
 file_d3 = '../writestr/dyn00800.txt'
 file_d4 = '../writestr/dyn00900.txt'
 file_d5 = '../writestr/dyn01000.txt'
}
if( iplot==5 ){
 file_d1 = '../writestr/dyn01200.txt'
 file_d2 = '../writestr/dyn01400.txt'
 file_d3 = '../writestr/dyn01600.txt'
 file_d4 = '../writestr/dyn01800.txt'
 file_d5 = '../writestr/dyn02000.txt'
}
if( iplot==6 ){
 file_d1 = '../writestr/dyn02200.txt'
 file_d2 = '../writestr/dyn02400.txt'
 file_d3 = '../writestr/dyn02600.txt'
 file_d4 = '../writestr/dyn02800.txt'
 file_d5 = '../writestr/dyn03000.txt'
}

set multiplot layout 2,1

set style line 10 ps 0.2 pt 1 lc 0 dt (7,10)

set style line 1 ps 0.2 pt 6 lc 1
set style line 2 ps 0.2 pt 6 lc 2
set style line 3 ps 0.2 pt 6 lc 3
set style line 4 ps 0.2 pt 6 lc 4
set style line 5 ps 0.2 pt 6 lc 5
set style line 6 ps 0.2 pt 6 lc rgb 'gold'
set style line 7 ps 0.2 pt 6 lc rgb 'forest-green'
set style line 8 ps 0.2 pt 6 lc rgb 'dark-gray'

set style line 11 ps 0.2 pt 6 dt (6,8) lc 0 lw 1
set style line 12 ps 0.2 pt 6 dt (6,8) lc 0 lw 1
set style line 13 ps 0.2 pt 6 dt (6,8) lc 0 lw 1
set style line 14 ps 0.2 pt 6 dt (2,3) lc 4
set style line 15 ps 0.2 pt 6 dt (2,3) lc 5

###
load 'plot_settings.gp'
###

###
load 'plot_rad_denspres.gp'
load 'plot_rad0_denspres.gp'
###

unset multiplot
