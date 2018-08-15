#!/bin/sh
# Shell script para instalar GR-Foo, GR-802.15.4 e GR-LQE no No-0
# Wendley S. Silva – wendley@gmail.com - Jul/2018


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

# Atualiza o arquivo mac de gr-802154, pois é o Nó 1 (muda só o endereco mac):
cp sdr/macNo1.cc gr-802154-wy/lib/mac.cc ;
cd ~;

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
# echo "\n Instalando GR-LQE... \n"
# echo "\n Descomprimindo os arquivos do GR-LQE... \n"
# sleep $pausa
#
# cd ~ ;
# tar -vzxf CodesGr2.tar.gz


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

############  GIT  ############


#wget https://raw.githubusercontent.com/wendley/Temp/master/InstalarXBee.sh


# One time, configure:
# git git config --global user.name "John Doe"
# git config --global user.email johndoe@example.com


# Inside the folder, do:

# git init
# git remote add origin https://wendley@bitbucket.org/wendley/gr-ieee802-15-4.git
# echo "Wendley S. Silva" >> contributors.txt
# git add contributors.txt
# git commit -m 'Initial commit with contributors'
# git push -u origin master
# git add -A
# git commit -m 'Initial commit'
# git push -u origin master
