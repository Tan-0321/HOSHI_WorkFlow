set xl  'lg rad'
set yl  'lg temp'
set y2l 'sk'
set ytics nomirror
set y2tics
set yr  [*:*]
set y2r [*:*]
plot \
file_w1                 u (log10(@i_rad)):(log10(@i_temp)) w l ls 1         ti 'temp',\
file_w1                 u (log10(@i_rad)):(@i_sk)          w l ls 2 ax x1y2 ti 'sk',\
file_w1  eve dj::(dj-1) u (log10(@i_rad)):(log10(@i_temp)) w p ls 1         ti '',\
file_w1  eve dj::(dj-1) u (log10(@i_rad)):(@i_sk)          w p ls 2 ax x1y2 ti ''

set xr [*:*]
unset y2l
unset y2tics