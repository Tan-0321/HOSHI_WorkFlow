set xl 'log B_{rad}'
set yl 'log P_{rot}'
set xr [*:*]
set yr [*:*]

plot \
file_summary           u (log10(filt(@k_ievo,0,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls 11 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,0,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls 11 ti '',\
file_summary           u (log10(filt(@k_ievo,1,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls  1 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,1,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls  1 ti '',\
file_summary           u (log10(filt(@k_ievo,2,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls  2 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,2,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls  2 ti '',\
file_summary           u (log10(filt(@k_ievo,3,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls  3 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,3,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls  3 ti '',\
file_summary           u (log10(filt(@k_ievo,4,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls  4 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,4,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls  4 ti '',\
file_summary           u (log10(filt(@k_ievo,5,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls  5 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,5,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls  5 ti '',\
file_summary           u (log10(filt(@k_ievo,6,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls  6 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,6,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls  6 ti '',\
file_summary           u (log10(filt(@k_ievo,7,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls  7 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,7,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls  7 ti '',\
file_summary           u (log10(filt(@k_ievo,8,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w l ls  8 ti '',\
file_summary eve dnstg u (log10(filt(@k_ievo,8,@k_Bsrf))):(log10(Prot(@k_Rsrf,@k_vrot))) w p ls  8 ti ''

unset xr
set xr [*:*]
