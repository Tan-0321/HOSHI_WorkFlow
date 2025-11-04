
set xl  'mass'
set yl  'lg dens'
set y2l 'lg temp'
set ytics nomirror
set y2tics
set yr  [*:*]
set y2r [*:*]
plot \
file_w1  u 3:(log10($9 )) w l ls 1         ti 'dens',\
file_w1  u 3:(log10($10)) w l ls 2 ax x1y2 ti 'temp'

unset y2l
unset y2tics