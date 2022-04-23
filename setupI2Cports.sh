#!/bin/bash

echo -e '\n#new i2c ports' | sudo tee -a /boot/config.txt
echo 'dtoverlay=i2c-gpio,bus=16,i2c_gpio_sda=22,i2c_gpio_scl=23' | sudo tee -a /boot/config.txt
echo 'dtoverlay=i2c-gpio,bus=15,i2c_gpio_sda=12,i2c_gpio_scl=13' | sudo tee -a /boot/config.txt
echo 'dtoverlay=i2c-gpio,bus=14,i2c_gpio_sda=10,i2c_gpio_scl=11' | sudo tee -a /boot/config.txt
echo 'dtoverlay=i2c-gpio,bus=13,i2c_gpio_sda=6,i2c_gpio_scl=9' | sudo tee -a /boot/config.txt
echo 'dtoverlay=i2c-gpio,bus=12,i2c_gpio_sda=8,i2c_gpio_scl=7' | sudo tee -a /boot/config.txt
echo 'dtoverlay=i2c-gpio,bus=11,i2c_gpio_sda=4,i2c_gpio_scl=5' | sudo tee -a /boot/config.txt
echo 'dtoverlay=i2c-gpio,bus=10,i2c_gpio_sda=0,i2c_gpio_scl=1' | sudo tee -a /boot/config.txt