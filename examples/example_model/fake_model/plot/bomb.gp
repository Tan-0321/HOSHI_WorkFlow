
set term pdf size 9,6
set outp "bomb.pdf"

nstg0 = 8150

file_summary = '../summary/summary.txt'
nstg_chr= sprintf("%05i",nstg0)
file_w0 = '../writestr/str'.nstg_chr.'.txt'

if( ARG1 eq "" ){ 
 print("plot last step")
 file_w1 = system('ls ../writestr/str*.txt | tail -n 1')
}else{
 nstg    = ARG1+0
 nstg_chr= sprintf("%05i",nstg)
 file_w1 = '../writestr/str'.nstg_chr.'.txt'
 print("plot nstg = ".ARG1)
}

txt_sys = 'head -n 1 '.file_w1.' | tail -n 1'
line  = system(txt_sys)
time  = line[35:45]
dtime = line[55:65]

call 'plot_thermalbomb.gp'