res

file1 = $0

set style line 10 lw 2 lt 1 lc rgb '#D53E4F' # 
set style line 11 lw 2 lt 1 lc rgb '#F46D43' #
set style line 12 lw 2 lt 1 lc rgb '#FDAE61' # 
set style line 13 lw 2 lt 1 lc rgb '#E6F598' #
set style line 14 lw 2 lt 1 lc rgb '#66C2A5' #
set style line 15 lw 2 lt 1 lc rgb '#3288BD' #

#set style line 20 lw 2 lt 4 lc rgb '#D53E4F' # 
#set style line 21 lw 2 lt 4 lc rgb '#F46D43' #
#set style line 22 lw 2 lt 4 lc rgb '#FDAE61' # 
#set style line 23 lw 2 lt 4 lc rgb '#E6F598' #
#set style line 24 lw 2 lt 4 lc rgb '#66C2A5' #

set style line 20 lw 2 lt 4 lc rgb '#3288BD' #

set multiplot

set lmargin 0
set rmargin 0
set tmargin 0
set bmargin 0

xsize = 0.38
ysize = 0.28
xorig = 0.11
yorig = 0.13

x11 = xorig
y11 = yorig + ysize * 2.0
x12 = xorig + xsize
y12 = yorig + ysize * 2.0
x21 = xorig
y21 = yorig + ysize * 1.0
x22 = xorig + xsize
y22 = yorig + ysize * 1.0
x31 = xorig
y31 = yorig + ysize * 0.0
x32 = xorig + xsize
y32 = yorig + ysize * 0.0

set size xsize,ysize

#set key r b
unset key


#cord(i,m,r) = mass(m)
#txt_xtics = 'mass'

#mass(x) = x
#xmin = 0.98
#xmax = 1.0

#mass(x) = log10(1.0-x+1e-30)
#xmin = -10
#xmax =  -3


#cord(i,m,r) = rad(r)
#txt_xtics = 'radius'

#rad(x) = x # * 7e10
#xmin = 0
#xmax = 1.2

#rad(x) = log10(9.317779128820E-01-x+1e-30)
#xmin = -5
#xmax =  0


cord(i,m,r) = mesh(i)
txt_xtics = 'mesh num'

mesh(i) = i
xmin = 620
xmax = 1028



flog(x) = x>0 ? log10(x) : 1/0



set xr [xmin:xmax]
set mxtics 
#set log y
#set log y2


set format x ""

set origin x11,y11
unset ytics
unset y2tics
set format y2 ""
set y2l ""

set format y 
set yl "Omega [10^{-4} rad s^{-1}]"
set yr [-2:2]
set ytics mirror
plot \
file1 u (cord($$1,$$2,$$3)):($$6/1e-4) w l ls 10




set format x ""

set origin x21,y21
unset ytics
unset y2tics
set format y2 ""
set y2l ""


set format y 
set yl "lg Eta"
set yr [5:15]
set ytics mirror
plot \
file1 u (cord($$1,$$2,$$3)):( $$11) w l ls 10 axis x1y1,\
file1 u (cord($$1,$$2,$$3)):( $$12) w l ls 20 axis x1y1






set format x
set xl txt_xtics

set origin x31,y31
unset ytics
unset y2tics
set format y2 ""
set y2l ""
set format y "%g"
#set yl "B_{phi} [10^7 G]"
#set yr [-3:3]
set yl "lg Bphi"
set yr [-5:5]
set ytics 1 mirror
plot \
file1 u (cord($$1,$$2,$$3)):(flog( $$9)) w l ls 10 ,\
file1 u (cord($$1,$$2,$$3)):(flog(-$$9)) w l ls 20 

#file1 u (cord($$1,$$2,$$3)):($$9/1e7) w l ls 10

####

set xr [xmin:xmax]
set mxtics 
#set log y
unset log y2


set format x ''
set xl ''

set origin x12,y12
unset ytics
unset y2tics
set format y ""
set yl ""
set format y2 
set y2l "dOdlnr"
set y2r [-12:1]
set y2tics mirror
plot \
file1 u (cord($$1,$$2,$$3)):(flog( $$7)) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$2,$$3)):(flog(-$$7)) w l ls 20 axis x1y2




set format x ''
set xl ''

set origin x22,y22
unset ytics
unset y2tics
set format y ""
set yl ""
set format y2 
set y2l "lg Alp"
set y2r [-10:10]
set y2tics mirror
plot \
file1 u (cord($$1,$$2,$$3)):(flog( $$19)) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$2,$$3)):(flog(-$$19)) w l ls 20 axis x1y2



set format x
set xl txt_xtics

set origin x32,y32
unset ytics
unset y2tics
set format y ""
set yl ""
set format y2 "%g"
unset log y2
#set y2l "dlnO/dr"
#set y2r [-7:0]
set y2l "lg Brad"
set y2r [-5:5]
set y2tics 1 mirror
plot \
file1 u (cord($$1,$$2,$$3)):(flog( $$8)) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$2,$$3)):(flog(-$$8)) w l ls 20 axis x1y2

#file1 u (cord($$1,$$2,$$3)):(flog( $$7)) w l ls 10 axis x1y2,\
#file1 u (cord($$1,$$2,$$3)):(flog(-$$7)) w l ls 20 axis x1y2


unset multiplot