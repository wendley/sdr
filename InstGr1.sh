#!/bin/sh
# Shell script para instalar GR-Foo e GR-802.15.4
# Wendley S. Silva – wendley@gmail.com - Jul/2018


git clone https://wendley@bitbucket.org/wendley/sdr.git;
cd sdr;
cp * ~/ ;
cd ~;


pausa=3

echo "\n Descomprimindo os arquivos... \n"
sleep $pausa

tar -vzxf UpGr1.tar.gz

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
# sleep $pausa
#
# cd ~ ;
# cd gr-lqe ;
# mkdir build ;
# cd build ;
# cmake .. ;
# make ;
# sudo make install ;
# sudo ldconfig ;


### GRC Compile ###
echo "\n Compilando ieee802_15_4_PHY.grc... \n"
sleep $pausa

cd ~ ;
cd gr-802154-wy/examples ;
grcc ieee802_15_4_OQPSK_PHY.grc ;
#grcc -e transceiver.grc ;


### Conclusao ###
echo "\n . \n .. \n ... \n Descompressao e compilacao concluidos \n ... \n .. \n ."



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
