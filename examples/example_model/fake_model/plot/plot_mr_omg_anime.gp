
set xl  'mass'
set yl  'Br'
set y2l 'Bp'
set ytics nomirror
set y2tics
set yr  [-2e3:2e3]
set y2r [-1e8:1e8]
plot \
file_w1                 u (@i_mr):( @i_Brad) w l ls  1         ti 'B_{rad}',\
file_w1                 u (@i_mr):( @i_Bphi) w l ls  2 ax x1y2 ti 'B_{phi}',\
file_w1  eve dj::(dj-1) u (@i_mr):( @i_Brad) w p ls  1         ti '',\
file_w1  eve dj::(dj-1) u (@i_mr):( @i_Bphi) w p ls  2 ax x1y2 ti '',\

unset y2l
unset y2tics