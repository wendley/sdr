#!/bin/sh
# Shell script para atualizar o arquivo getRSSI.py do modulo gr-LQE
# Wendley S. Silva – wendley@gmail.com - Jul/2018

if [ $# -lt 1 ]; then
   echo "Faltou informar o numero do Nó, 0 ou 1 ou 2 etc."
   exit 1
fi

cd ~/ ;
rm sdr/ -rf ;
git clone https://github.com/wendley/sdr.git ;
cd sdr;
cp * ~/ ;
cd ~;
pausa=0
sleep $pausa

case $1 in
   "0") cp sdr/macRX.cc gr-802154-wy/lib/mac.cc ;
        echo "MAC - Node RX"
        touch no.RX ;
        ;;
   "1") #Altera somente o endereco mac:
        cp sdr/macTX1.cc gr-802154-wy/lib/mac.cc ;
        echo "MAC - Node TX 1"
        touch no.TX1 ;
        cd ~;
        ;;
   "2") # Atualiza o arquivo mac de gr-802154, pois é o Nó 2 (muda somente o endereco mac):
        cp sdr/macTX2.cc gr-802154-wy/lib/mac.cc ;
        echo "MAC - Node TX 2"
        touch no.TX2 ;
        cd ~;
        ;;
   "3") # Atualiza o arquivo mac de gr-802154, pois é o Nó 3 (muda somente o endereco mac):
        cp sdr/macTX3.cc gr-802154-wy/lib/mac.cc ;
        echo "MAC - Node TX 3"
        touch no.TX3 ;
        cd ~;
        ;;
   "4") # Atualiza o arquivo mac de gr-802154, pois é o Nó 4 (muda somente o endereco mac):
        cp sdr/macTX4.cc gr-802154-wy/lib/mac.cc ;
        echo "MAC - Node TX 4"
        touch no.TX4 ;
        cd ~;
        ;;
   *) echo "Opção inválida!"
        exit 1
        ;;
esac

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
