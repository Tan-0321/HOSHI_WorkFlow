#!/usr/bin/sh
rm fgtmp*

rm -r -f cxdata
rm -r -f pgfile
rm -r -f pngfile
rm -r -f strdata
rm -r -f summary
rm -r -f writestr
rm -f stream.dat
mkdir cxdata
mkdir pgfile
mkdir pngfile
mkdir strdata
mkdir summary
mkdir writestr

#rm evol
#cp ${HOSHI_DIR}/${HOSHI_version}/bin/evol .
sh copy_HOSHI.sh

#cp ../250413_hydro/strdata/m1.5e1_z1.0e0_0.bin strdata/.
#cp ../250413_hydro/cxdata/cxdat08146.txt cxdata/.
cp strdata_e/* strdata/.
cp cxdata_e/* cxdata/.

