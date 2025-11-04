set xl 'log Rsrf'
set yl 'log L'
set xr [] rev
set yr [*:*]

plot \
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,0,@k_mtot))) w l ls 11 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,0,@k_mtot))) w p ls 11 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,1,@k_mtot))) w l ls  1 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,1,@k_mtot))) w p ls  1 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,2,@k_mtot))) w l ls  2 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,2,@k_mtot))) w p ls  2 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,3,@k_mtot))) w l ls  3 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,3,@k_mtot))) w p ls  3 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,4,@k_mtot))) w l ls  4 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,4,@k_mtot))) w p ls  4 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,5,@k_mtot))) w l ls  1 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,5,@k_mtot))) w p ls  1 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,6,@k_mtot))) w l ls  2 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,6,@k_mtot))) w p ls  2 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,7,@k_mtot))) w l ls  3 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,7,@k_mtot))) w p ls  3 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,8,@k_mtot))) w l ls  8 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,8,@k_mtot))) w p ls  8 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,9,@k_mtot))) w l ls  4 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,9,@k_mtot))) w p ls  4 ti '',\
file_summary           u (log10(@k_Rsrf)):(log10(filt(@k_mlos,10,@k_mtot))) w l ls 5 ti '',\
file_summary eve dnstg u (log10(@k_Rsrf)):(log10(filt(@k_mlos,10,@k_mtot))) w p ls 5 ti ''

unset xr
set xr [*:*]
