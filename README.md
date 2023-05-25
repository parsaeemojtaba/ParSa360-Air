# ParSa 360+Air: A 360-degree Imagery-Multisensory Capture System

## Installation

To install all the required libraries and dependencies, run the following command lines in a terminal:

   ```
   git clone https://github.com/parsaeemojtaba/ParSa360.git
   chmod 777 /home/pi/ParSa360/Install.sh
   ./Install.sh
   ```
## Description of Raspberry Pi Dependency Installation and Update Script

This script automates the installation of dependencies and performs system updates on a Raspberry Pi device. It includes the following tasks:

- Install Dependencies: Pandas, Thermal Cam, CO2, PM2.5.
- System Updates: Update and upgrade packages.
- Move Run File: Transfer `ParSaDataLoggerSet.py` to the main directory.

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
