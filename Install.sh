#!/bin/bash

## set I2C ports
echo "$(tput setaf 10)set I2C ports"
echo -e "\n#new i2c ports" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2c-gpio,bus=16,i2c_gpio_sda=22,i2c_gpio_scl=23" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2c-gpio,bus=15,i2c_gpio_sda=12,i2c_gpio_scl=13" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2c-gpio,bus=14,i2c_gpio_sda=10,i2c_gpio_scl=11" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2c-gpio,bus=13,i2c_gpio_sda=6,i2c_gpio_scl=9" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2c-gpio,bus=12,i2c_gpio_sda=8,i2c_gpio_scl=7" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2c-gpio,bus=11,i2c_gpio_sda=4,i2c_gpio_scl=5" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2c-gpio,bus=10,i2c_gpio_sda=0,i2c_gpio_scl=1" | sudo tee -a /boot/config.txt

## clone ParSa360 files
# echo "$(tput setaf 10)clone ParSa360 files"
# if ! (git clone https://github.com/parsaeemojtaba/ParSa360.git) then
#     echo "$(tput setaf 9)cannot clone the repository!"
#     echo "cannot clone the repository!" | sudo tee -a /home/pi/info.txt
# else
#     echo "$(tput setaf 11)done!"
#     echo "done!" | sudo tee -a /home/pi/info.txt
# fi

## install pandas
echo "$(tput setaf 10)install pandas"
sudo apt-get install python3-pandas

## install Thermal Cam
echo "$(tput setaf 10)install Thermal Cam"
pip3 install Seeed-grove.py
pip3 install seeed-python-mlx9064x

## install CO2
echo "$(tput setaf 10)install CO2"
sudo pip3 install mh-z19

## install PM2.5
echo "$(tput setaf 10)install PM2.5"
sudo pip3 install adafruit-circuitpython-pm25
sudo pip3 install pyserial

## update and ugrade
echo "$(tput setaf 10)update and ugrade"
sudo apt-get update
sudo apt-get upgrade

## move the run file to main dirctory
echo "$(tput setaf 10)move the run file to main dirctory"
sudo mv /home/pi/ParSa360/ParSaDataLoggerSet.py /home/pi/ParSaDataLoggerSet.py

