#!/bin/bash

cd ../plot
gnuplot anime.gp

cd fpdf
namelist=`ls fpdf-*.pdf`
for fpdf in $namelist; do
 echo 'converting: '$fpdf
 fpng=../fpng/fpng-${fpdf:5:5}.png
 convert -density 400 -background white $fpdf $fpng
done

cd ../fpng
ffmpeg -r 30 -i fpng-%04d0.png -vcodec libx264 -pix_fmt yuv420p -s 1920x1080 anime.mp4
mv anime.mp4 ../../anime/.

cd ../
