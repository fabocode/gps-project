#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/pi/gps-project/setup/
sudo pip3 install -r requirements.txt
sudo python3 install_kivy.py 
cd /
