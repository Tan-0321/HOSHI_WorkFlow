
set xl  'mass'
set yl  'lg X'
set ytics mirror
set yr [-6:0.2]
plot \
file_w1  u 3:(log10($18)) w l ls 1  ti 'H',\
file_w1  u 3:(log10($19)) w l ls 2  ti 'He',\
file_w1  u 3:(log10($20)) w l ls 3  ti 'C',\
file_w1  u 3:(log10($21)) w l ls 4  ti 'N',\
file_w1  u 3:(log10($22)) w l ls 5  ti 'O'
