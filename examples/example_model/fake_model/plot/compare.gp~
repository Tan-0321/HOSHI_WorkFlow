file1 = "../summary/summary.txt"
file2 = "../../fc0.05_fmu0.1/summary/summary.txt"

set xl "lgTeff"
set xr [] rev
set yl "lgLum"

plot \
file1 u (log10($16)):(log10($15)) w l ti "modif.",\
file2 u (log10($16)):(log10($15)) w l ti "orig."
