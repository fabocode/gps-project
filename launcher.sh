#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

#cd /
#bluetoothctl << EOF
#power on
#EOF

cd /
cd home/pi/Documents/GPS_TRACKING_SYSTEM
sudo pigpiod
sudo python gui.py
cd /
