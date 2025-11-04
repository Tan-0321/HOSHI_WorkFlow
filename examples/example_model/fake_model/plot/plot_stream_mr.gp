res

set term pdf size 5,8
set outp 'stream_mr.pdf'

file='../summary/stream_mr.txt'

set style line 10 lw 0.2 lc rgb 'gray'
set style line 11 lw 0.6 lc rgb 'black'

set multiplot layout 2,1

unit = 1.
set yl 'mass [M_{sun}]'

ix   = '$2'
set xr [1e-3:]
set xl 'time [s]'
load 'plot_stream_lines2.gp'

ix   = '$1'
set xr [1e-3:]
set xl 'step #'
load 'plot_stream_lines2.gp'
