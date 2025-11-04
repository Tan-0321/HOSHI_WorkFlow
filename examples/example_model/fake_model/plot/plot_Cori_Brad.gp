set xl 'log Teff'
set yl 'log taucv'
set xr [] rev
set yr [*:*]


plot \
file_summary           u (log10(@i_Teff)):(log10(filt(@i_ievo,0,1./$26))) w l ls 11 ti '',\
file_summary eve dnstg u (log10(@i_Teff)):(log10(filt(@i_ievo,0,1./$26))) w p ls 11 ti '',\
file_summary           u (log10(@i_Teff)):(log10(filt(@i_ievo,1,1./$26))) w l ls  1 ti '',\
file_summary eve dnstg u (log10(@i_Teff)):(log10(filt(@i_ievo,1,1./$26))) w p ls  1 ti '',\
file_summary           u (log10(@i_Teff)):(log10(filt(@i_ievo,2,1./$26))) w l ls  2 ti '',\
file_summary eve dnstg u (log10(@i_Teff)):(log10(filt(@i_ievo,2,1./$26))) w p ls  2 ti ''


#,\
file_summary           u (log10(@i_time)):(log10(filt(@i_ievo,7,1./$28))) w l ls  2 ti '',\
file_summary eve dnstg u (log10(@i_time)):(log10(filt(@i_ievo,7,1./$28))) w p ls  2 ti ''

unset xr
set xr [*:*]
