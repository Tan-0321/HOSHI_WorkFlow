
set xl  'mass'
set yl  'lg vel'
set ytics mirror
set yr [-6:13]
plot \
file_w1  u ($1):(log10( @i_rad/(dtime*3.15e7)))    w l ls  1   ti 'R/dtime',\
file_w1  u ($1):(log10( @i_vcv))                   w l ls  3   ti 'vcv',\
file_w1  u ($1):(log10( @i_vrot))                  w l ls  5   ti 'vrot*',\
file_w1  u ($1):(log10(-@i_vrot))                  w l ls 15   ti '',\
file_w1  u ($1):(log10( @i_alp))                   w l ls  2   ti 'alp',\
file_w1  u ($1):(log10(-@i_alp))                   w l ls 12   ti '',\
file_w1  u ($1):(log10( @i_vel))                   w l ls  4   ti 'v',\
file_w1  u ($1):(log10(-@i_vel))                   w l ls 14   ti '',\
file_w1  u ($1):(log10( @i_cs ))                   w l ls  6   ti 'cs',\
file_w1  u ($1):(log10( @i_cs )-1)                 w l ls  6 lw 0.1 ti '',\
file_w1  u ($1):(log10( @i_cs )-2)                 w l ls  6 lw 0.1 ti '',\
file_w1  u ($1):(log10( @i_cs )-3)                 w l ls  6 lw 0.1 ti '',\
file_w1  u ($1):(log10( @i_cs )-4)                 w l ls  6 lw 0.1 ti '',\
file_w1 eve dj::(dj-1)  u ($1):(log10( @i_rad/(dtime*3.15e7)))    w p ls  1   ti '',\
file_w1 eve dj::(dj-1)  u ($1):(log10(@i_vcv))     w p ls  3   ti ''


