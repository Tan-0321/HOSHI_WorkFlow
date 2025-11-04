res

file = '../yield/abund.dat'

set term pdf 
set outp 'abund.pdf'

set xl 'proton number'
set xr [0.5:30.5]
set mxtics
set yl '[X/O]'
set yr [-3:3]

set key l t at graph 0.03, graph 0.85

set style line 10 pt 5 ps 0.2 dt 2 lc 'cyan'
set style line 11 pt 7 ps 0.2 dt 1 lc rgb '#B2182B' # red
set style line 12 pt 7 ps 0.2 dt 1 lc rgb '#D6604D' # red-orange
set style line 13 pt 7 ps 0.2 dt 1 lc rgb '#F4A582' # 
set style line 14 pt 7 ps 0.2 dt 1 lc rgb '#FDDBC7' # pale orange
set style line 15 pt 7 ps 0.2 dt 1 lc rgb '#D1E5F0' # pale blue
set style line 16 pt 7 ps 0.2 dt 1 lc rgb '#92C5DE' # 
set style line 17 pt 7 ps 0.2 dt 1 lc rgb '#4393C3' # medium blue
set style line 18 pt 7 ps 0.2 dt 1 lc rgb '#2166AC' # dark blue


plot \
file eve 2::2 u 1:(2.7):2  w labels ti '',\
file eve 2::1 u 1:(2.5):2  w labels ti '',\
file u 1:3  w lp ls 10 ti 'prog',\
file u 1:4  w lp ls 11 ti 'M_{bomb}',\
file u 1:5  w lp ls 12 ti '1.5',\
file u 1:6  w lp ls 13 ti '1.6',\
file u 1:7  w lp ls 14 ti '1.7',\
file u 1:8  w lp ls 15 ti '1.8',\
file u 1:9  w lp ls 16 ti '1.9',\
file u 1:10 w lp ls 17 ti '2.0',\
file u 1:11 w lp ls 18 ti '2.1'
