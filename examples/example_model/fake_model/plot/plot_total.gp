
set xl 'lg rest time [sec]'
set yl 'lg |Etot|'
set xr [] rev
set yr [*:*]

set y2l 'lg Jtot'
set ytics nomirror
set y2tics
set y2r [*:*]

plot \
etot           u (rtime[$1]):2     w l         ls  1 ti '|Etot|',\
etot eve dnstg u (rtime[$1]):2     w p         ls  1 ti '',\
mtot           u (rtime[$1]):2     w l ax x1y2 ls  2 ti 'Mtot',\
mtot eve dnstg u (rtime[$1]):2     w p ax x1y2 ls  2 ti ''

#jtot           u (rtime[$1]):2     w l ax x1y2 ls  2 ti 'Jtot',\
#jtot eve dnstg u (rtime[$1]):2     w p ax x1y2 ls  2 ti ''

unset xr
set xr [*:*]
unset yr

unset y2l
unset y2tics