#!/bin/sh
# Shell script para instalar GR-Foo e GR-802.15.4
# Wendley S. Silva – wendley@gmail.com - Jul/2018


cd ~/ ;
rm sdr -rf ;
git clone https://github.com/wendley/sdr.git ;
# cd sdr;
# cp * ~/ ;
# cd ~;

cp sdr/getRSSI.py gr-lqe/python ;

pausa=3

echo "\n Removendo GR-LQE... \n"
sleep $pausa

cd ~ ;
cd gr-lqe ;
cd build ;

sudo make uninstall ;

# cd .. ;
# rm build -rf ;

### GR-LQE ###
echo "\n Reinstalando GR-LQE... \n"
sleep $pausa

# cd ~ ;
# cd gr-lqe ;
# mkdir build ;
# cd build ;
#cmake .. ;
# make ;
sudo make install ;
sudo ldconfig ;


### GRC Compile ###
# echo "\n Compilando ieee802_15_4_PHY.grc... \n"
# sleep $pausa
#
# cd ~ ;
# cd gr-802154-wy/examples ;
# grcc ieee802_15_4_OQPSK_PHY.grc ;
# #grcc -e transceiver.grc ;




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
