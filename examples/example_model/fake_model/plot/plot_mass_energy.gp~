set xl 'log mtot'
set yl 'log Lrad'
set xr [*:*]
set yr [*:*]

plot \
file_summary           u (log10(@k_mtot)):(log10(@k_Lrad)) w l ls  1 ti 'Lrad',\
file_summary eve dnstg u (log10(@k_mtot)):(log10(@k_Lrad)) w p ls  1 ti ''    ,\
file_summary           u (log10(@k_mtot)):(log10(@k_Lnuc)) w l ls  2 ti 'Lnuc',\
file_summary eve dnstg u (log10(@k_mtot)):(log10(@k_Lnuc)) w p ls  2 ti ''    

#,\
#file_summary           u (log10(@k_mtot)):(log10(@k_Lnu )) w l ls  3 ti 'Lnu',\
#file_summary eve dnstg u (log10(@k_mtot)):(log10(@k_Lnu )) w p ls  3 ti ''

unset xr
set xr [*:*]
