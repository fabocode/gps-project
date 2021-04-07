import threading
import time
import gps_data
import RPi.GPIO as IO

x = 0
flag = False
gps = gps_data.GPS

# GPS Class
init_gps = gps()

# Setup the  GPS Device
gps.setup_skytraq_gps(init_gps)

def loop_thread():
    try:    
        while flag == False:
            gps.update_gps_time(init_gps)
            #print("gps seconds inside thread: {}".format(gps.seconds))
    except KeyboardInterrupt:
        IO.cleanup()
        sys.exit



try:
    my_thread = threading.Thread(target=loop_thread) # instance the thread
    my_thread.start()   # call to start the thread
    while True:
        x = 0    
        #gps.update_gps_time(init_gps)
        print("gps_seconds outside thread: {}". format(gps.seconds))
        time.sleep(1)

except KeyboardInterrupt:
    flag = True
    IO.cleanup()
    sys.exit
