set xl 'log mtot'
set yl 'log Lrad'
set xr [*:*]
set yr [*:*]

plot \
file_summary           u (log10(@k_mtot)):(log10(@k_Lrad)) w l ls  1 ti 'Lrad',\
file_summary eve dnstg u (log10(@k_mtot)):(log10(@k_Lrad)) w p ls  1 ti ''

unset xr
set xr [*:*]
