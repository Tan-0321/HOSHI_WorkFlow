res

set term pdf font 'Helvetica,8' size 4,3

title='HOSHI eostest'
foutp='plot/plot_eostest.pdf'
fload='eostest.dat'

set outp foutp
file = fload

x00   = 0.04
y00   = 0.05
xsize = 0.49
ysize = 0.49

#load 'plot_range.gp'
set xl 'lg dens'
set yl 'lg temp'


#fplt(x) = log10(x)
fplt(x) = (x> 1e5)? log10( x):\
        ( (x<-1e5)?-log10(-x):\
	   asinh(0.5*x)/log(10) )
#print fplt(9.9e4),log10(9.9e4),fplt(-1e10)
#exit

set view map scale 1
set    samples 50,50
set isosamples 51,51
unset surface

set contour base
set cntrparam levels 20
#set cntrparam levels incremental -50,2,50
set cntrparam cubicspline
set cntrlabel onecolor
set cntrlabel format '%8.3g' font ',5' start 2 interval 50
set style textbox opaque margins 0.5,0.5 fc bgnd noborder linewidth 1.0
set style line 11 lw 0.6 dt  1    lc rgb 'sienna1'
set style line 12 lw 0.6 dt (3,2) lc rgb 'sienna1'
set style line 21 lw 0.3 dt  1    lc rgb 'sea-green'
set style line 22 lw 0.3 dt (3,2) lc rgb 'sea-green'

set multiplot
set lmargin 0
set rmargin 0
set tmargin 0
set bmargin 0



set size xsize,ysize
set key r b box opaque font ',6'


xorig = x00
yorig = y00 + ysize
set label title at graph 0.02, 1.07
set orig xorig,yorig
splot \
file u (log10($5)):(log10($6)):(log10( $7)) w l ls 11 ti 'pos.',\
file u (log10($5)):(log10($6)):(log10(-$7)) w l ls 12 ti 'neg.',\
file u (log10($5)):(log10($6)):(log10( $7)) w labels boxed ti '',\
file u (log10($5)):(log10($6)):(log10(-$7)) w labels boxed ti ''


xorig = x00
yorig = y00
unset label
set label 'd/dln dens' at graph 0.02, 1.07
set orig xorig,yorig
splot \
file u (log10($5)):(log10($6)):(log10( $8)) w l ls 11 ti 'val.',\
file u (log10($5)):(log10($6)):(log10(-$8)) w l ls 12 ti '',\
file u (log10($5)):(log10($6)):(log10( $8)) w labels boxed ti '',\
file u (log10($5)):(log10($6)):(log10(-$8)) w labels boxed ti '',\
file u (log10($5)):(log10($6)):(log10( $9)) w l ls 21 ti 'num.',\
file u (log10($5)):(log10($6)):(log10(-$9)) w l ls 22 ti ''


xorig = x00 + xsize
yorig = y00 + ysize
unset label
set label 'd/dln temp' at graph 0.02, 1.07
set orig xorig,yorig
splot \
file u (log10($5)):(log10($6)):(log10( $10)) w l ls 11 ti 'val.',\
file u (log10($5)):(log10($6)):(log10(-$10)) w l ls 12 ti '',\
file u (log10($5)):(log10($6)):(log10( $10)) w labels boxed ti '',\
file u (log10($5)):(log10($6)):(log10(-$10)) w labels boxed ti '',\
file u (log10($5)):(log10($6)):(log10( $11)) w l ls 21 ti 'num.',\
file u (log10($5)):(log10($6)):(log10(-$11)) w l ls 22 ti ''



unset multiplot