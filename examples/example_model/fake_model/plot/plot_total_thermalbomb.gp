
set xl 'time [sec]'
set yl 'Eexp [1e51]'
set xr []
set yr [*:*]

plot \
file_summary           u (log10($5)):($8/1e51)     w l         ls  1 ti 'Etot',\
file_summary eve dnstg u (log10($5)):($8/1e51)     w p         ls  1 ti '',\

unset xr
unset yr
