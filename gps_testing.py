import Peripherals as peripherals
import time

# instance gps class from peripherals module/lib
gps = peripherals.GPS

# Gps class
init_gps = gps()

# Setup the GPS device
gps.setup_skytraq_gps(init_gps)

# measure 5 seconds loop to check gps synchronization
time_gps_ok = 0
time_gps_check = time.time()
time_gps_result = 0

# wait 5 seconds to restart gps module in case of failures
gps_running_ok = 0 #time.time()
gps_failed = 0
gps_result = 0


# wait 2 seconds to save gps data to compare 
min_time_running = 0
min_time_result = time.time() #0
min_time_last = 0

# save hours, minutes and seconds
h_gps = "0"
m_gps = "0"
s_gps = "0.0"

last_h = "0"
last_m = "0"
last_s = "0"

wh = "24"
wm = "0"
ws = "0"

# handle gps status
gps_status = True

def isTimeFormat(h, m, s):
    try:
        max_seconds = 59.99
        if (float(s) > max_seconds):
            return False
        else:
            stopwatch = "{}:{}:{}".format(h, m, s)
            time.strptime(stopwatch, "%H:%M:%S.%f")
            return True
    except ValueError:
        return False

def check_gps_time(gps_running_time):
    global time_gps_check
    return int(gps_running_time - time_gps_check)
    #return time_gps_result

def min_check_gps(min_time_gps):
    global min_time_result
    return int(min_time_gps - min_time_result)

while True:

    time_gps_ok = time.time()

    min_time_running = time.time()
    
    if min_check_gps(min_time_running) > 1:
        min_time_result = time.time()
        last_h = h_gps
        last_m = m_gps
        last_s = s_gps
        #print("check gps ")

    #print("time gps result {}".format(check_gps_time(time_gps_ok)))
    if check_gps_time(time_gps_ok) > 5:
        # after 5 seconds, restart the timer and check gps sync
        time_gps_check = time.time()
        if "{}:{}:{}".format(last_h, last_m, last_s) == "{}:{}:{}".format(h_gps, m_gps, s_gps):
            gps_status = False 
        print("last data {}:{}:{} and new data {}:{}:{}".format(last_h, last_m, last_s, h_gps, m_gps, s_gps))
    
    if gps_status == True:

        # get gps data 
        gps.update_gnss_data(init_gps)

        # save gps running time 
        gps_running_ok = time.time()

        # check gps format data
        #gps_status = isTimeFormat(wh, wm, ws)
        gps_status = isTimeFormat(h_gps, m_gps, s_gps)
        #print("time format is: {} and time is: {}:{}:{}".format(gps_status, h_gps, m_gps, s_gps))
        
        if gps_status == True:
            # save gps data   
            h_gps = str(gps.hours)
            m_gps = str(gps.minutes)
            s_gps = str(gps.seconds)
    else:
        gps_failed = time.time()
        gps_result = int(gps_failed - gps_running_ok)
        
        if gps_result == 10:
            gps_status = True
            gps_running_ok = time.time()
            print("reset gps status to True ")
        #print("time status: {} - and WITHOUT data: {}".format(gps_status, gps_result))

