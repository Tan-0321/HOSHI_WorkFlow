
set xl  'mass'
if( imass_range==1 ){
    set xr [@mass_min:@mass_max]
}
set yl  'lg X'
set ytics mirror
set yr [-6:0.2]
plot \
file_w0  u (@i_mr):(log10(@i_C )) w l ls 1  ti 'C0',\
file_w0  u (@i_mr):(log10(@i_Ne)) w l ls 2  ti '"Ne0"',\
file_w0  u (@i_mr):(log10(@i_Si)) w l ls 3  ti '"Si0"',\
file_w0  u (@i_mr):(log10(@i_Fe)) w l ls 4  ti '"Fe0"',\
file_w0  eve dj::(dj-1) u (@i_mr):(log10(@i_C )) w p ls 1  ti '',\
file_w0  eve dj::(dj-1) u (@i_mr):(log10(@i_Ne)) w p ls 2  ti '',\
file_w0  eve dj::(dj-1) u (@i_mr):(log10(@i_Si)) w p ls 3  ti '',\
file_w0  eve dj::(dj-1) u (@i_mr):(log10(@i_Fe)) w p ls 4  ti '',\
\
file_w1  u (@i_mr):(log10(@i_C )) w l ls 5  ti 'C',\
file_w1  u (@i_mr):(log10(@i_Ne)) w l ls 6  ti '"Ne"',\
file_w1  u (@i_mr):(log10(@i_Si)) w l ls 7  ti '"Si"',\
file_w1  u (@i_mr):(log10(@i_Fe)) w l ls 8  ti '"Fe"',\
file_w1  eve dj::(dj-1) u (@i_mr):(log10(@i_C )) w p ls 5  ti '',\
file_w1  eve dj::(dj-1) u (@i_mr):(log10(@i_Ne)) w p ls 6  ti '',\
file_w1  eve dj::(dj-1) u (@i_mr):(log10(@i_Si)) w p ls 7  ti '',\
file_w1  eve dj::(dj-1) u (@i_mr):(log10(@i_Fe)) w p ls 8  ti ''

set xr [*:*]