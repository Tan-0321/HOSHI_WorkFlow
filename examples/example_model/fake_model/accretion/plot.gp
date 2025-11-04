res

set outp "plot.pdf"
set term pdf

file_summary = "../summary/summary.txt"
year = 3.15e7
J0   = 1e50
mdot = 1e-3
jdot = mdot * 1.99e33 * 1e17

set style line 1  lw 2 lc "orange"  dt 1
set style line 2  lw 2 lc "cyan" dt 1

set style line 11 lw 1 lc "red"  dt 2
set style line 12 lw 1 lc "blue" dt 2

set key l t

set xl "step number"
set yl "q"

set log y
plot \
file_summary u 1:7             w l ls 1  ti "mass"