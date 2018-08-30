#!/bin/sh
# Shell script para atualizar o arquivo getRSSI.py do modulo gr-LQE
# Wendley S. Silva – wendley@gmail.com - Jul/2018


cd ~/ ;
rm sdr/ -rf ;
git clone https://github.com/wendley/sdr.git ;
cd sdr;
cp * ~/ ;
cd ~;
pausa=1
sleep $pausa

cp mac.cc gr-802154-wy/lib/ ;

sleep $pausa
echo "\n Removendo GR-802154-WY... \n"

cd ~ ;
cd gr-802154-wy/build ;
sudo make uninstall ;

# cd .. ;
# rm build -rf ;

### GR-LQE ###
echo "\n Reinstalando GR-802154-WY... \n"
sleep $pausa

# cd ~ ;
# cd gr-lqe ;
# mkdir build ;
# cd build ;
#cmake .. ;
# make ;
sudo make install ;
sudo ldconfig ;
