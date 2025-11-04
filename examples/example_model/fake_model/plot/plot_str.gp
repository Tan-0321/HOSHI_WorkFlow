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

set style line 30 lw 1 lt 4 lc 2

set multiplot

set lmargin 0
set rmargin 0
set tmargin 0
set bmargin 0

xsize = 0.24
ysize = 0.28
xorig = 0.11
yorig = 0.13

x11 = xorig
y11 = yorig + ysize * 2.0
x21 = xorig
y21 = yorig + ysize * 1.0
x31 = xorig
y31 = yorig + ysize * 0.0

x12 = xorig + xsize
y12 = yorig + ysize * 2.0
x22 = xorig + xsize
y22 = yorig + ysize * 1.0
x32 = xorig + xsize
y32 = yorig + ysize * 0.0

x13 = xorig + xsize * 2.0
y13 = yorig + ysize * 2.0
x23 = xorig + xsize * 2.0
y23 = yorig + ysize * 1.0
x33 = xorig + xsize * 2.0
y33 = yorig + ysize * 0.0

set size xsize,ysize

#set key r b
unset key


#cord(i,m,r) = mass(m)
#txt_xtics = 'mass'

#mass(x) = x
#xmin = 0
#xmax = 1.1

#mass(x) = log10(1.0-x+1e-30)
#xmin = -10
#xmax =  -3


#cord(i,m,r) = rad(r)
#txt_xtics = 'radius'

#rad(x) = 10**x # * 7e10
#xmin = 0
#xmax = 1.6

#rad(x) = log10(9.317779128820E-01-x+1e-30)
#xmin = -5
#xmax =  0


cord(i,m,r) = mesh(i)
txt_xtics = 'mesh num'

mesh(i) = i
xmin = 1
xmax = 1025




flog(x) = x>0 ? log10(x) : 1/0
Beq(lgrho,vcv) = flog( sqrt(4.*3.14*10**lgrho)*vcv )

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
set yl "lg Omega"
set yr [-7:-3]
set ytics mirror
plot \
file1 u (cord($$1,$$3,$$5)):(flog( $$33)) w l ls 10,\
file1 u (cord($$1,$$3,$$5)):(flog(-$$33)) w l ls 20




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
file1 u (cord($$1,$$3,$$5)):(flog($$64)) w l ls 10 axis x1y1,\
file1 u (cord($$1,$$3,$$5)):(flog($$47)) w l ls 20 axis x1y1






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
file1 u (cord($$1,$$3,$$5)):(flog( $$58)) w l ls 10 ,\
file1 u (cord($$1,$$3,$$5)):(flog(-$$58)) w l ls 20 ,\
file1 u (cord($$1,$$3,$$5)):(Beq($$9,$$56)) w l ls 30


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
file1 u (cord($$1,$$3,$$5)):(flog( $$61)) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$3,$$5)):(flog(-$$61)) w l ls 20 axis x1y2




set format x ''
set xl ''

set origin x22,y22
unset ytics
unset y2tics
set format y ""
set yl ""
set format y2 
set y2l "lg Alp"
set y2r [0:7]
set y2tics mirror
plot \
file1 u (cord($$1,$$3,$$5)):(flog( $$62)) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$3,$$5)):(flog(-$$62)) w l ls 20 axis x1y2



set format x
set xl txt_xtics

set origin x32,y32
unset ytics
unset y2tics
set format y ""
set yl ""
set format y2 "%g"
unset log y2
set y2l "lg Brad"
set y2r [-5:5]
set y2tics 1 mirror
plot \
file1 u (cord($$1,$$3,$$5)):(flog( $$59)) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$3,$$5)):(flog(-$$59)) w l ls 20 axis x1y2,\
file1 u (cord($$1,$$3,$$5)):(Beq($$9,$$56)) w l ls 30 axis x1y2




####

set xr [xmin:xmax]
set mxtics 
#set log y
unset log y2


set format x ''
set xl ''

set origin x13,y13
unset ytics
unset y2tics
set format y ""
set yl ""
set format y2 
set y2l "lgT, lgrho"
set y2r [*:*]
set y2tics mirror
plot \
file1 u (cord($$1,$$3,$$5)):($$10) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$3,$$5)):($$9 ) w l ls 20 axis x1y2




set format x ''
set xl ''

set origin x23,y23
unset ytics
unset y2tics
set format y ""
set yl ""
set format y2 
set y2l "nabla"
set y2r [*:0.5]
set y2tics mirror
plot \
file1 u (cord($$1,$$3,$$5)):($$42) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$3,$$5)):($$41) w l ls 20 axis x1y2



set format x
set xl txt_xtics

set origin x33,y33
unset ytics
unset y2tics
set format y ""
set yl ""
set format y2 "%g"
unset log y2
set y2l "lg X,Y"
set y2r [-3:0.3]
set y2tics 1 mirror
plot \
file1 u (cord($$1,$$3,$$5)):(flog($$18)) w l ls 10 axis x1y2,\
file1 u (cord($$1,$$3,$$5)):(flog($$19)) w l ls 20 axis x1y2


unset multiplot