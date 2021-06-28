'''
    NOTE: Run with `sudo`
'''
import os 

def install_node():
    '''
        This script install node js to the raspberry pi
    '''
    os.system('sudo apt update')
    os.system('curl -sL https://deb.nodesource.com/setup_15.x | bash -')
    os.system('apt-get install -y nodejs')
    os.system('clear')
