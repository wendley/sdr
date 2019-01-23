#!/bin/sh
# Shell script para enviar atualizacoes locais para GitHub
# Wendley S. Silva – wendley@gmail.com - Jan/2019

NOW=$(date +"%d/%m/%Y") ;

cdsdr; # alias Linux: alias cdsdr='cd ~/Dropbox/Documentos/PhD/Codigos/sdr/'

cp ../gr-lqe/python/getRSSI.py sdr/ ;
cp ../gr-lqe/grc/lqe_getRSSI.xml sdr/ ;
cp ../gr-lqe/python/powerControl.py sdr/ ;

cdsdr;
git add . ;
git commit -m "atualizacao de $NOW" ;
git push;

# sleep 1
echo "\n ... \n Encerrando script \n ..."
sleep 0.3
