import os, time 

def install_requirements():
    os.system('sudo pip3 install -r requirements.txt')

def setup_gps():
    '''
        NOTE: it's also required to do the following:
            1. Go to terminal 
            2. type sudo raspi-config
            3. enable UART 
            4. Disable the serial login shell console 
            5. Save and reboot.
    '''
    os.system("sed -i '/\[all\]/a dtoverlay=pi3-miniuart-bt' /boot/config.txt")

def install_pigpio():
    os.system('wget https://github.com/joan2937/pigpio/archive/master.zip')
    os.system('unzip master.zip')
    os.system('cd pigpio-master && make')
    os.system('cd pigpio-master && sudo make install')

def install_kivy():
    '''
        system will call an script to import kivy called 'kivy_importer.py'
        this is required to create ~/.kivy/ folder 
        and add the touchscreen feature automatically
    '''
    os.system('sudo apt update')
    os.system('sudo apt install pkg-config libgl1-mesa-dev libgles2-mesa-dev libgstreamer1.0-dev gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-{omx,alsa} libmtdev-dev xclip xsel libjpeg-dev')
    os.system('sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev')
    os.system('sudo python3 -m pip install kivy[base] kivy_examples')
    os.system('sudo python3 kivy_importer.py') 
    time.sleep(1) # give time to system to call and end this program 

def setup_touchscreen_input():
    '''
        Enable the touch screen feature in display
    ''' 
    os.system("sed -i '/\[input\]/a hid_%(name)s = probesysfs,provider=hidinput' ~/.kivy/config.ini")
    os.system("sed -i '/\[input\]/a mtdev_%(name)s = probesysfs,provider=mtdev' ~/.kivy/config.ini")

def reboot_system():
    os.system('sudo reboot')

if __name__ == '__main__':
    try:
        install_requirements()
        install_pigpio()
        install_kivy() # install kivy
        setup_touchscreen_input() # enable touchscreen 
        setup_gps()
        reboot_system() 
        

    except Exception as e:
        print(f"it does not work: {e}")
