import os 

def install_node():
    os.system('sudo apt update')
    os.system('curl -sL https://deb.nodesource.com/setup_15.x | bash -')
    os.system('apt-get install -y nodejs')
    os.system('clear')
    