set term pdf
set outp "HR.pdf"

# m3
file1 = "../../summary/summary.txt.m3e0"
n1_ZAMS = 555
n1_TAMS = 707
n1_f00  = n1_ZAMS
n1_f01  = 565 -1
n1_f02  = 573 -1
n1_f03  = 582 -1
n1_f04  = 592 -1
n1_f05  = 603 -1
n1_f06  = 615 -1
n1_f07  = 629 -1
n1_f08  = 647 -1
n1_f09  = 670 -1
n1_f10  = n1_TAMS

# m8e0
file2 = "../../summary/summary.txt.m8e0"
n2_ZAMS = 315
n2_TAMS = 476
n2_f00  = n2_ZAMS
n2_f01  = 565 -1
n2_f02  = 573 -1
n2_f03  = 582 -1
n2_f04  = 592 -1
n2_f05  = 603 -1
n2_f06  = 615 -1
n2_f07  = 629 -1
n2_f08  = 647 -1
n2_f09  = 670 -1
n2_f10  = n2_TAMS

# m7e0
file3 = "../../mshells/m7e0/summary/summary.txt"
n3_ZAMS = 400
n3_TAMS = 980
n3_f00  = n3_ZAMS
n3_f01  = 565 -1
n3_f02  = 573 -1
n3_f03  = 582 -1
n3_f04  = 592 -1
n3_f05  = 603 -1
n3_f06  = 615 -1
n3_f07  = 629 -1
n3_f08  = 647 -1
n3_f09  = 670 -1
n3_f10  = n3_TAMS


set xl "lg Teff"
set yl "lg L/Lsun"
set xr [3.85:*] rev
set xtics 0.05
set ytics 0.1
set mxtics
set mytics



set style line  1 lw 0.5 dt 1 lc "blue"
set style line  2 lw 2 dt 1 lc "blue" pt 7 ps 0.4
set style line  3 lw 0.5 dt 1 lc "blue"
set style line  4 lw 2 pt 7 lc "red" ps 0.5

set key r t box opaque
plot \
"HR_CUVir.dat" u (log10($1)):2:($3/$1/log(10.)):4 w xyerrorbars ti "CU Vir, Sikora+19" ls 4,\
"HR_V901Ori.dat" u (log10($1)):2:($3/$1/log(10.)):4 w xyerrorbars ti "V901 Ori, Simbad" ls 4,\
file1 u (log10($16)):(log10($15)) eve ::(n1_ZAMS-10)::n1_ZAMS  w l ls 1 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_ZAMS::n1_TAMS       w l ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_TAMS::(n1_TAMS+300) w l ls 3 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f00::n1_f00         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f01::n1_f01         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f02::n1_f02         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f03::n1_f03         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f04::n1_f04         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f05::n1_f05         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f06::n1_f06         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f07::n1_f07         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f08::n1_f08         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f09::n1_f09         w p ls 2 ti "",\
file1 u (log10($16)):(log10($15)) eve ::n1_f10::n1_f10         w p ls 2 ti "",\
\
file2 u (log10($16)):(log10($15)) eve ::(n2_ZAMS-10)::n2_ZAMS  w l ls 1 ti "",\
file2 u (log10($16)):(log10($15)) eve ::n2_ZAMS::n2_TAMS       w l ls 2 ti "",\
file2 u (log10($16)):(log10($15)) eve ::n2_TAMS::(n2_TAMS+300) w l ls 3 ti "",\
\
file3 u (log10($16)):(log10($15)) eve ::(n3_ZAMS-10)::n3_ZAMS  w l ls 1 ti "",\
file3 u (log10($16)):(log10($15)) eve ::n3_ZAMS::n3_TAMS       w l ls 2 ti "",\
file3 u (log10($16)):(log10($15)) eve ::n3_TAMS::(n3_TAMS+300) w l ls 3 ti ""

# check n-nstg relation
res
#set xl "nstg"
#set xr [n_f00-3:n_f02+3]
#set mxtics
#plot \
file1 u ($1):(log10($15)) eve ::n_f00::n_f00         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f01::n_f01         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f02::n_f02         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f03::n_f03         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f04::n_f04         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f05::n_f05         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f06::n_f06         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f07::n_f07         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f08::n_f08         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f09::n_f09         w p ls 2 ti "",\
file1 u ($1):(log10($15)) eve ::n_f10::n_f10         w p ls 2 ti ""
