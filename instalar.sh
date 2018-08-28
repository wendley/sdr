#!/bin/sh
# Shell script para instalar GR-Foo, GR-802.15.4, GR-LQE etc.
# Wendley S. Silva – wendley@ufc.br - Ago/2018
# ------
# Usar da seguinte forma:
# ./Instalar 0   ou    ./Instalar 1 etc.


if [ $# -lt 1 ]; then
   echo "Faltou informar o numero do Nó, 0 ou 1"
   exit 1
fi

NumeroNo=$1 ;


git clone https://github.com/wendley/sdr.git ;
cd sdr ;
cp * ~/ ;
cd ~;
mkdir Experimentos ;


pausa=2

echo "\n Descomprimindo os arquivos... \n"
sleep $pausa

tar -vzxf CodesGr1.tar.gz ;

# Atualiza o arquivo getRSSI:
cp sdr/getRSSI.py gr-lqe/python ;
cd ~;

# Atualiza o arquivo mac de gr-802154
cp sdr/mac.cc gr-802154-wy/lib/ ;
cd ~;


case $1 in
   "0") echo "MAC - No zero"
         ;;
   "1") # Atualiza o arquivo mac de gr-802154, pois é o Nó 1 (muda só o endereco mac):
         cp sdr/macNo1.cc gr-802154-wy/lib/mac.cc ;
         echo "MAC - No 1"
         cd ~;
         ;;
   *) echo "Opção inválida!"
      exit 1
      ;;
esac

# exit;

### GR-FOO ###
echo "\n Instalando GR-FOO... \n"
sleep $pausa

cd ~ ;
cd gr-foo ;
mkdir build ;
cd build ;
cmake .. ;
make ;
sudo make install ;
sudo ldconfig ;


### GR-IEEE802-15-4 - versão WY ###
echo "\n Instalando GR-IEEE802-15-4 versao Wy... \n"
sleep $pausa

#cd ~ ; cd gr-802154-wy ; mkdir build ; cd build ; cmake .. ; make ; sudo make install ; sudo ldconfig ;
cd ~ ;
cd gr-802154-wy ;
mkdir build ;
cd build ;
cmake .. ;
make ;
sudo make install ;
sudo ldconfig ;


### GR-EVENTSTREAM ###
echo "\n Instalando GR-EVENTSTREAM... \n"
# Dependencias: BOOST e PKG-CONFIG
# sudo apt-get install libboost-all-dev
# sudo apt-get install pkg-config
sleep $pausa

cd ~ ;
cd gr-eventstream ;
mkdir build ;
cd build ;
cmake .. ;
make ;
sudo make install ;
sudo ldconfig ;



### GR-UHDGPS ###
echo "\n Instalando GR-UHDGPS... \n"
sleep $pausa

cd ~ ;
cd gr-uhdgps ;
mkdir build ;
cd build ;
cmake .. ;
make ;
sudo make install ;
sudo ldconfig ;


### GR-LQE ###
echo "\n Instalando GR-LQE... \n"
sleep $pausa

cd ~ ;
cd gr-lqe ;
mkdir build ;
cd build ;
cmake .. ;
make ;
sudo make install ;
sudo ldconfig ;


### GRC Compile ###
echo "\n Compilando ieee802_15_4_PHY.grc... \n"
sleep $pausa

cd ~ ;
cd gr-802154-wy/examples ;
grcc ieee802_15_4_OQPSK_PHY.grc ;
#grcc -e transceiver.grc ;


echo "\n Instalando GR-TRAFFICGEN... \n"
sleep $pausa

cd ~ ;
cd gr-trafficgen ;
mkdir build ;
cd build ;
cmake .. ;
make ;
sudo make install ;
sudo ldconfig ;


### Conclusao ###
echo "\n . \n .. \n ... \n Descompressao e compilacao concluidos \n ... \n .. \n ."
sleep $pausa

cd ~ ;
echo "\n Atualizando PIP e instalando scikit-learn... \n"
sleep $pausa
sudo pip install --upgrade pip ;
sudo pip install -U scikit-learn ;

cd ~ ;
chmod +x atualizar.sh ;
chmod +x clone.sh ;

cd gr-802154-wy/examples ;

# echo "\n . \n .. Removendo pasta temporaria sdr \n .. \n ."
# sleep $pausa
#
# cd ~/ ;
# rm sdr/ -rf ;
