
set xl  'mass'
if( imass_range==1 ){
    set xr [@mass_min:@mass_max]
}
set yl  'lg dens'
set y2l 'lg temp'
set ytics nomirror
set y2tics
set yr  [*:*]
set y2r [*:*]
dj = 2*6
plot \
file_w1  u 3:(log10($9 )) w l ls 1         ti 'dens',\
file_w1  u 3:(log10($10)) w l ls 2 ax x1y2 ti 'temp',\
file_w1  eve dj::(dj-1) u 3:(log10($9 )) w p ls 1         ti '',\
file_w1  eve dj::(dj-1) u 3:(log10($10)) w p ls 2 ax x1y2 ti ''

unset y2l
unset y2tics