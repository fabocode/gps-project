import Peripherals as peripherals
import threading
##import gps_data
import time
import RPi.GPIO as IO


# Define GPIOs
RPM_SENSOR_PIN = 5
TEMP_SENSOR_ADDR = 0x5A
# Define GPIO Mode
GPIO_MODE = IO.BCM
# Define other parameters
TIRE_RADIUS_REF = 13.1 # Inch
TIRE_PRESSURE_REF = 33 # Pressure of reference

sense = peripherals.Sensors
record = peripherals.Record

# testing
gps = peripherals.GPS
#gps = gps_data.GPS


# dataToStrings = peripherals.dataToStrings
SET_VALUE_RECORD = True

flag = False


def loop_thread():
    while flag == False:
       #gps.update_gps_time(init_gps)
       gps.update_gnss_data(init_gps)  # get gps data
       #print("gps seconds inside thread: {}".format(gps.seconds))

try:
    # Classes
    # Sensors peripheral class
    init_sense = sense(
    GPIO_MODE,
    RPM_SENSOR_PIN)#,
    #TEMP_SENSOR_ADDR
    #)
    # Record class
    init_record = record()
    
    # testing
    # Gps class
    init_gps = gps()
    #init_gps = gps()
    
    # dataToStrings class
    # init_strings = dataToStrings()


    # testing
    # Setup the GPS device
    gps.setup_skytraq_gps(init_gps)
    #gps.setup_skytraq_gps(init_gps)
    # Set temperature of reference
    #sense.set_temperature_ref(init_sense)

    i = 0

    my_thread = threading.Thread(target=loop_thread)  # instance the thread
    my_thread.start()   # call to start the thread

    while True:
        '''
        record.start_record(init_record)
        i = i + 1
        resultado_time = int(time.time() - record.the_time)
        print(resultado_time)
        if(record.toggle_status == 0):
            if(resultado_time >= 5):
                print('5 seconds is elapsed')
        elif(record.toggle_status == 1):
            if(resultado_time >= 10):
                print('10 seconds is elapsed')
        '''
        #print("gps_seconds outside thread: {}". format(gps.seconds))
        #time.sleep(1)
        #sense.temperature_read(init_sense) # Call this function to refresh the temperature values
        record.set_record(init_record, SET_VALUE_RECORD) # Call this function to set Record button status
        record.start_record(init_record) # Call this function to start recording if all condition succeeds
        sense.speed_calc(init_sense, TIRE_RADIUS_REF, TIRE_PRESSURE_REF)	# Call this function with tire radius as parameter
        #gps.update_gnss_data(init_gps) # Update gnss TIRE_RADIUS_REF incoming data from GPS
        #gps.update_gps_time(init_gps)
        #record.timer_switch(init_record)
        #print("sw_time: {}".format(record.sw_time))
        #print("time: {}".format(record.tm))
        #print("record.t: {}".format(record.t))
        #print("set_record_time: {}".format(record.set_record_time))
        #print("current time: {}".format(time.time()))
        #print("time: {}:{}:{}".format(record.recorded_time["hours"], record.recorded_time["minutes"], record.recorded_time["seconds"]))
        #time.sleep(1)


        #dataToStrings.toStrings(init_strings)


        #print(dataToStrings.dist_miles)

        #print("Vehicle Info. ==>> rpm:{0}-RPM speed:{1}-MPH dist_meas:{2}-MI pulses:{3} timer:{4}:{5}:{6} TT:{7}C,{8}F AT:{9}C,{10}F".format(
        #sense.rpm,
        #sense.mph,
        #sense.dist_meas,
        #sense.pulses,
        #record.recorded_time["hours"],
        #record.recorded_time["minutes"],
        #record.recorded_time["seconds"],
        #sense.temperature["tire_C"],
        #sense.temperature["tire_F"],
        #sense.temperature["ambient_C"],
        #sense.temperature["ambient_F"]
        #))

        print("GPS Info. ==>> date:{0}/{1}/{2} UTC_time:{3}:{4}:{5} latitude:{6} longitude:{7} speed:{8}-MPH \n".format(
        gps.month,
        gps.day,
        gps.year,
        gps.hours,
        gps.minutes,
        gps.seconds,
        gps.latitude,
        gps.longitude,
        gps.speed_in_mph
        ))
        time.sleep(1)
        #print("UTC_TIME: {0}:{1}:{2}".format(gps.hours, gps.minutes, gps.seconds))

        #print("Speed accurracy: {0}".format(record.mph_accurate))

        #time.sleep(0.001)
        #i = i + 1
        #print("seconds elapsed: {} seconds".format(i))
       # time.sleep(.01)
        #print("my_difference: {}".format(record.my_difference))
        #time.sleep(0.1)
        #print('Record.toggle_button_time %s ' % (round(record.toggle_button_time)))
        #print('Record.the_time %s ' % (round(record.the_time)))
        #print('Record.last_toggle_time %f ' % (record.last_toggle_time))
        #print('record.set_record_time %s ' % (record.set_record_time))
        #print('record.toggle_button_time %s ' % (record.toggle_button_time))
        #time.sleep(.5)

except KeyboardInterrupt:
    flag = True
    IO.cleanup()
    sys.exit








