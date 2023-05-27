#!/bin/bash

## install pandas
echo "$(tput setaf 12)install pandas"
sudo apt-get install python3-pandas

## install pyqt
echo "$(tput setaf 6)install pyqt5"
sudo apt-get install python3-pyqt5
sudo apt-get install qt5-style-plugins

## install Thermal Cam
echo "$(tput setaf 12)install Thermal Cam"
pip3 install Seeed-grove.py
pip3 install seeed-python-mlx9064x

## install CO2
echo "$(tput setaf 6)install CO2"
sudo pip3 install mh-z19

## install PM2.5
echo "$(tput setaf 12)install PM2.5"
sudo pip3 install adafruit-circuitpython-pm25
sudo pip3 install pyserial

## update and ugrade
echo "$(tput setaf 6)update and ugrade"
sudo apt-get update
sudo apt-get upgrade

## set I2C ports
chmod 777 /home/pi/ParSa360-Air/libs/setI2Cs.sh  
/home/pi/ParSa360-Air/libs/setI2Cs.sh

## move the run file to main dirctory
echo "$(tput setaf 12)move the run file to main dirctory"
sudo mv /home/pi/ParSa360-Air/libs/runlogger.py /home/pi/
sudo mv /home/pi/ParSa360-Air/libs/runlogger_gui.py /home/pi/
