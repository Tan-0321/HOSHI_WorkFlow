res

set term pdf size 100,10
set outp 'check.pdf'

file='../check.log'

set style line 1 lc 1 pt 5 ps 0.1
set style line 2 lc 2 pt 6 ps 0.1

set xr [*:*]
set log y
plot \
file eve :2::0 u 2:(abs($3)) w lp ls 1 ,\
file eve :2::1 u 2:(abs($3)) w lp ls 2 
