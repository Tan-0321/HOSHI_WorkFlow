set xl 'log Rossby (=Prot/tcv)'
set yl 'log Brad [G]'
set xr [*:*]
set yr [*:*]


plot \
file_summary           u (log10(@k_Rossby)):(log10(filt(@k_ievo,0,@k_Bsrf))) w l ls 11 ti '',\
file_summary eve dnstg u (log10(@k_Rossby)):(log10(filt(@k_ievo,0,@k_Bsrf))) w p ls 11 ti '',\
file_summary           u (log10(@k_Rossby)):(log10(filt(@k_ievo,1,@k_Bsrf))) w l ls  1 ti '',\
file_summary eve dnstg u (log10(@k_Rossby)):(log10(filt(@k_ievo,1,@k_Bsrf))) w p ls  1 ti '',\
file_summary           u (log10(@k_Rossby)):(log10(filt(@k_ievo,2,@k_Bsrf))) w l ls  2 ti '',\
file_summary eve dnstg u (log10(@k_Rossby)):(log10(filt(@k_ievo,2,@k_Bsrf))) w p ls  2 ti ''


#,\
file_summary           u (log10(@k_time)):(log10(filt(@k_ievo,7,1./$28))) w l ls  2 ti '',\
file_summary eve dnstg u (log10(@k_time)):(log10(filt(@k_ievo,7,1./$28))) w p ls  2 ti ''

unset xr
set xr [*:*]
