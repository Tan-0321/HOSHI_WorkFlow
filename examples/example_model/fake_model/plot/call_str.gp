
set term gif animate optimize delay 5 size 720,540
set output "evol_str_omg7d-2.gif" 

nmin = 820
nmax =2600
dn   = 5

imin = (nmin-nmin) / dn #+ 1 - 1/dn
imax = (nmax-nmin) / dn
do for [i=imin:imax] {

 n = i*dn + nmin

 if( 0     <=n & n<=9    ){ nmodel = "0000".n }
 if( 10    <=n & n<=99   ){ nmodel = "000".n  }
 if( 100   <=n & n<=999  ){ nmodel = "00".n   }
 if( 1000  <=n & n<=9999 ){ nmodel = "0".n    }
 if( 10000<=n            ){ nmodel = n        }

 filename = "writestr/str".nmodel.".txt"
 call "plot_str.gp" filename

 if( i%50 == 0 ){ print filename }

}
