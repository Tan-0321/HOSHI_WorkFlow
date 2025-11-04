
set xl  'mass'
if( imass_range==1 ){
    set xr [@mass_min:@mass_max]
}
set yl  'lg B_{rad}'
set yr  [*:*]
plot \
file_w1                 u (@i_mr):(log_pos(Beq(@i_vcv ,@i_dens))) w l ls  3 ti 'B_{cv}',\
file_w1                 u (@i_mr):(log_pos(Beq(@i_vrot,@i_dens))) w l ls  4 ti 'B_{rot}',\
file_w1                 u (@i_mr):(log_neg(Beq(@i_vrot,@i_dens))) w l ls 14 ti '',\
\
file_w1                 u (@i_mr):(log_pos(@i_Brad)) w l ls  1 ti 'B_{rad}',\
file_w1                 u (@i_mr):(log_pos(@i_Bphi)) w l ls  2 ti 'B_{phi}',\
file_w1                 u (@i_mr):(log_neg(@i_Brad)) w l ls 11 ti '',\
file_w1                 u (@i_mr):(log_neg(@i_Bphi)) w l ls 12 ti '',\
file_w1  eve dj::(dj-1) u (@i_mr):(log_pos(@i_Brad)) w p ls  1 ti '',\
file_w1  eve dj::(dj-1) u (@i_mr):(log_pos(@i_Bphi)) w p ls  2 ti '',\
file_w1  eve dj::(dj-1) u (@i_mr):(log_neg(@i_Brad)) w p ls 11 ti '',\
file_w1  eve dj::(dj-1) u (@i_mr):(log_neg(@i_Bphi)) w p ls 12 ti '',\

#\
#file_w1                 u (@i_mr):(log10( @i_Brad_im)) w l ls  3         ti 'B_{rad,i}',\
#file_w1                 u (@i_mr):(log10( @i_Bphi_im)) w l ls  4 ax x1y2 ti 'B_{phi,i}',\
#file_w1                 u (@i_mr):(log10(-@i_Brad_im)) w l ls 13         ti '',\
#file_w1                 u (@i_mr):(log10(-@i_Bphi_im)) w l ls 14 ax x1y2 ti '',\
#file_w1  eve dj::(dj-1) u (@i_mr):(log10( @i_Brad_im)) w p ls  3         ti '',\
#file_w1  eve dj::(dj-1) u (@i_mr):(log10( @i_Bphi_im)) w p ls  4 ax x1y2 ti '',\
#file_w1  eve dj::(dj-1) u (@i_mr):(log10(-@i_Brad_im)) w p ls 13         ti '',\
#file_w1  eve dj::(dj-1) u (@i_mr):(log10(-@i_Bphi_im)) w p ls 14 ax x1y2 ti ''

unset y2l
unset y2tics