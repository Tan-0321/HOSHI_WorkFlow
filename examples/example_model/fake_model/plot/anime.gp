nmin =  10
nmax =5000
dn   =  10

imin = (nmin-nmin) / dn #+ 1 - 1/dn
imax = (nmax-nmin) / dn
do for [i=imin:imax] {

 n = i*dn + nmin

 if( 0    <=n & n<=9    ){ nmodel = "0000".n }
 if( 10   <=n & n<=99   ){ nmodel = "000".n  }
 if( 100  <=n & n<=999  ){ nmodel = "00".n   }
 if( 1000 <=n & n<=9999 ){ nmodel = "0".n    }
 if( 10000<=n           ){ nmodel = n        }

 set term pdf size 5,3

 foutpdf = "fpdf/fpdf-".nmodel.".pdf"
 file_summary = '../summary/summary.txt'
 file_w1 = '../writestr/str'.nmodel.'.txt'

 txt_sys = 'head -n 1 '.file_w1.' | tail -n 1'
 line  = system(txt_sys)
 dtime = line[55:65]

 set outp foutpdf
 call 'plot_anime.gp'
# call 'plot_main.gp'

 if( i%50 == 0 ){ print foutpdf }

}
