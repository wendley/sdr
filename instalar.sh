#!/bin/sh
# Shell script para instalar GR-Foo, GR-802.15.4, GR-LQE etc.
# Wendley S. Silva – wendley@ufc.br - Jan/2019
# ------
# Usar da seguinte forma:
# ./instalar 0   ou    ./instalar 1 etc.


if [ $# -lt 1 ]; then
   echo "Faltou informar o numero do Nó, 0 (Rx) ou 1 ou 2 etc. para Tx"
   exit 1
fi

sudo ifconfig ens3 mtu 1400 up

git clone https://github.com/wendley/sdr.git ;
cd sdr ;
cp * ~/ ;
cd ~;
mkdir Experimentos ;

pausa=2

echo "\n ------------------------------\n"
echo "\n Descomprimindo os arquivos... \n"
echo "\n ------------------------------\n"
sleep $pausa
tar -vzxf CodesGr1.tar.gz ;


# Atualiza os arquivos getRSSI e mac de gr-80214:
cp sdr/getRSSI.py gr-lqe/python ;
cp sdr/powerControl.py gr-lqe/python ;
cp sdr/contador.py gr-lqe/python ;
cp sdr/lqe_getRSSI.xml gr-lqe/grc ;
cd ~;


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

# exit;


compilar()
{
  mkdir build ; cd build ; cmake .. ; make ; sudo make install ; sudo ldconfig ;
}

### GR-FOO ###
echo "\n ------------------------------\n"
echo "\n Instalando GR-FOO-2016... \n"
echo "\n ------------------------------\n"
sleep $pausa

cd ~ ;
cd gr-foo-2016 ;
compilar ; #funcao compilar



### GR-IEEE802-15-4 - versão WY ###
echo "\n ------------------------------\n"
echo "\n Instalando GR-IEEE802-15-4 versao Wy... \n"
echo "\n ------------------------------\n"
sleep $pausa

#cd ~ ; cd gr-802154-wy ; mkdir build ; cd build ; cmake .. ; make ; sudo make install ; sudo ldconfig ;
cd ~ ;
cd gr-802154-wy ;
compilar ; #funcao compilar


### GR-EVENTSTREAM ###
echo "\n ------------------------------\n"
echo "\n Instalando GR-EVENTSTREAM... \n"
echo "\n ------------------------------\n"
# Dependencias: BOOST e PKG-CONFIG
# sudo apt-get install libboost-all-dev
# sudo apt-get install pkg-config
sleep $pausa

cd ~ ;
cd gr-eventstream ;
compilar ; #funcao compilar



### GR-UHDGPS ###
echo "\n ------------------------------\n"
echo "\n Instalando GR-UHDGPS... \n"
echo "\n ------------------------------\n"
sleep $pausa

cd ~ ;
cd gr-uhdgps ;
compilar ; #funcao compilar


### GR-LQE ###
echo "\n ------------------------------\n"
echo "\n Instalando GR-LQE... \n"
echo "\n ------------------------------\n"
sleep $pausa

cd ~ ;
cd gr-lqe ;
compilar ; #funcao compilar


### COMPILANDO GR-802-15-4 ###
echo "\n ------------------------------\n"
echo "\n Compilando ieee802_15_4_PHY.grc... \n"
echo "\n ------------------------------\n"
sleep $pausa

cd ~ ;
cd gr-802154-wy/examples ;
grcc ieee802_15_4_OQPSK_PHY.grc ;
#grcc -e transceiver.grc ;


# echo "\n Instalando GR-TRAFFICGEN... \n"
# sleep $pausa
#
# cd ~ ;
# cd gr-trafficgen ;
# compilar ; #funcao compilar
#
# # Compilar Bloco Hierarquico TrafficGenHier
# cd ~;
# grcc TrafficGenHier.grc ;

### Conclusao ###
echo "\n ------------------------------\n"
echo "\n . \n .. \n ... \n Descompressao e compilacao concluidos \n ... \n .. \n ."
echo "\n ------------------------------\n"
sleep $pausa

cd ~ ;
echo "\n ------------------------------\n"
echo "\n Atualizando PIP e instalando scikit-learn e pandas... \n"
echo "\n ------------------------------\n"
sleep $pausa
sudo pip install --upgrade pip ;
sudo pip install -U scikit-learn ;
sudo pip install -U pandas ;

cd ~ ;
chmod +x recompilarMac.sh ;
chmod +x recompilarLQE.sh ;
chmod +x clone.sh ;

# cd gr-802154-wy/examples ;

# echo "\n . \n .. Removendo pasta temporaria sdr \n .. \n ."
# sleep $pausa
#
# cd ~/ ;
# rm sdr/ -rf ;

###########################################
#
## INSTALACAO DO PY-ADWIN - CONCEPT drift
#
###########################################

cd ~ ;
echo "\n ------------------------------\n"
echo "\n Instalando pyAdwin - Concept Drift Detection... \n"
echo "\n ------------------------------\n"

git clone https://github.com/rsdevigo/pyAdwin.git ;
cd pyAdwin && sudo python setup.py install
