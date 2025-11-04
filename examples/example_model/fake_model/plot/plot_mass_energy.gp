set xl 'log mtot'
set yl 'log Etot'
set xr [*:*]
set yr [*:*]

plot \
file_summary           u (log10(@k_mtot)):(log10(-@k_etot)) w l ls  1 ti 'Etot',\
file_summary eve dnstg u (log10(@k_mtot)):(log10(-@k_etot)) w p ls  1 ti ''    

#,\
#file_summary           u (log10(@k_mtot)):(log10(@k_Lnu )) w l ls  3 ti 'Lnu',\
#file_summary eve dnstg u (log10(@k_mtot)):(log10(@k_Lnu )) w p ls  3 ti ''

unset xr
set xr [*:*]
