
set xl  'mass'
set yl  'lg D  or lg nu'
set ytics mirror
set yr [0:22]
plot \
file_w1  u 3:(log10($5*$5*7e10*7e10/1e10)) w l ls 1   ti 'R2/1e10',\
file_w1  u 3:(log10($32)) w l ls 2   ti 'Dchem'
