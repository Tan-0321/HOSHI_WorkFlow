
set xl  'mass'
set yl  'lg eps'
set ytics mirror
set yr [-5:15]
plot \
file_w1  u 3:(log10( $26)) w l ls 1   ti 'eps',\
file_w1  u 3:(log10(-$26)) w l ls 11  ti '',\
file_w1  u 3:(log10( $27)) w l ls 2   ti 'epnu',\
file_w1  u 3:(log10(-$27)) w l ls 12  ti ''
