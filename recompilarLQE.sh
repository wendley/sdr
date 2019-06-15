#!/bin/sh
# Shell script para atualizar o arquivo getRSSI.py do modulo gr-LQE
# Wendley S. Silva – wendley@gmail.com - Jul/2018


cd ~/ ;
rm sdr/ -rf ;
git clone https://github.com/wendley/sdr.git ;
cd sdr;
cp * ~/ ;
cd ~;
pausa=0
sleep $pausa

cp getRSSI.py gr-lqe/python ;
cp contador.py gr-lqe/python ;
cp powerControl.py gr-lqe/python ;
cp lqe_getRSSI.xml gr-lqe/grc ;


# rm getRSSI.py; mv getRSSI-PRR.py getRSSI.py; cp getRSSI.py gr-lqe/python ; cd ~ ; cd gr-lqe ; cd build ; sudo make uninstall ; sudo make install ; sudo ldconfig ;

sleep $pausa
echo "\n Removendo GR-LQE... \n"


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
