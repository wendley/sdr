#!/bin/sh
# Shell script para atualizar o arquivo getRSSI.py do modulo gr-LQE
# Wendley S. Silva – wendley@gmail.com - Jul/2018


cd ~/ ;
rm sdr/ -rf ;
git clone https://github.com/wendley/sdr.git ;
cd sdr;
cp * ~/ ;
cd ~;

cd ~ ;
chmod +x atualizar.sh ;
chmod +x clone.sh ;
