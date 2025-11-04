
set xl  'lg rad'
set yl  'lg eps'
set ytics nomirror
set y2tics
set yr [-2:18]
set y2l 'nabla'
set y2r [-0.2:1.6]
plot \
file_w1  u (log10(@i_rad)):(log10( @i_enuc)) w l ls 1   ti 'e_{nuc}',\
file_w1  u (log10(@i_rad)):(log10(-@i_enuc)) w l ls 11  ti '',\
file_w1  u (log10(@i_rad)):(log10( @i_enu )) w l ls 2   ti 'e_{nu}',\
file_w1  u (log10(@i_rad)):(log10(-@i_enu )) w l ls 12  ti '',\
file_w1  u (log10(@i_rad)):(log10( @i_eent)) w l ls 3   ti 'e_{ent}',\
file_w1  u (log10(@i_rad)):(log10(-@i_eent)) w l ls 13  ti '',\
file_w1  u (log10(@i_rad)):(( @i_ncv )) w l ls 4 ax x1y2 ti 'n_{cv}',\
file_w1  u (log10(@i_rad)):(( @i_nrad)) w l ls 5 ax x1y2 ti 'n_{rad}',\
file_w1  u (log10(@i_rad)):(( @i_nmu )) w l ls 6 ax x1y2 ti 'n_{mu}',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10( @i_enuc)) w p ls 1   ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10(-@i_enuc)) w p ls 11  ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10( @i_enu )) w p ls 2   ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10(-@i_enu )) w p ls 12  ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10( @i_eent)) w p ls 3   ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10(-@i_eent)) w p ls 13  ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(( @i_ncv )) w p ls 4 ax x1y2 ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(( @i_nrad)) w p ls 5 ax x1y2 ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(( @i_nmu )) w p ls 6 ax x1y2 ti ''

#set y2l 'lg nabla'
#set y2r [-2:2]
#plot \
file_w1  u (log10(@i_rad)):(log10( @i_enuc)) w l ls 1   ti 'e_{nuc}',\
file_w1  u (log10(@i_rad)):(log10(-@i_enuc)) w l ls 11  ti '',\
file_w1  u (log10(@i_rad)):(log10( @i_enu )) w l ls 2   ti 'e_{nu}',\
file_w1  u (log10(@i_rad)):(log10(-@i_enu )) w l ls 12  ti '',\
file_w1  u (log10(@i_rad)):(log10( @i_ncv )) w l ls 4 ax x1y2 ti 'n_{cv}',\
file_w1  u (log10(@i_rad)):(log10( @i_nrad)) w l ls 5 ax x1y2 ti 'n_{rad}',\
file_w1  u (log10(@i_rad)):(log10( @i_nmu )) w l ls 6 ax x1y2 ti 'n_{mu}',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10( @i_enuc)) w p ls 1   ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10(-@i_enuc)) w p ls 11  ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10( @i_enu )) w p ls 2   ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10(-@i_enu )) w p ls 12  ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10( @i_ncv )) w p ls 4 ax x1y2 ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10( @i_nrad)) w p ls 5 ax x1y2 ti '',\
file_w1 eve dj::(dj-1)  u (log10(@i_rad)):(log10( @i_nmu )) w p ls 6 ax x1y2 ti ''

set xr [*:*]
unset y2l
unset y2tics
