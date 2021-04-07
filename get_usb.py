import os
import datetime
import shutil
from shutil import copytree, ignore_patterns

files = os.listdir('/media/user/')

destination = '/home/pi/Get_USB/Backup/back_%s'%datetime.datetime.now()
try :
    for f in files:
        source = '/media/user/%s' % f
        copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))    
except Exception as e:
    print e
