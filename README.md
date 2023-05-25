# ParSa 360+Air: A 360-degree Imagery-Multisensory Capture System

## Installation

To install all the required libraries and dependencies, run the following command lines in a terminal:

   ```
   git clone https://github.com/parsaeemojtaba/ParSa360-Air.git
   chmod 777 /home/pi/ParSa360/Install.sh
   ./Install.sh
   ```
## Description

This script automates the installation of dependencies and performs system updates on the Raspberry Pi device used in ParSa360+Air. It includes the following tasks:

- Install Dependencies: Pandas, Thermal Cam, CO2, PM2.5.
- Write I2C ports and update and upgrade OS packages.
- Move the file ‘ParSaDataLoggerSet.py’ to the home directory

To use this script, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/parsaeemojtaba/ParSa360.git
2. Set permissions for the installation script:

   ```
   chmod 777 /home/pi/ParSa360/Install.sh
3. Run the script:
   ```
   ./Install.sh
This will automate the setup process and ensure that all necessary dependencies are installed on your Raspberry Pi device.
Feel free to make any necessary adjustments to the above instructions to suit your specific needs.
