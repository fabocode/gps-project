"""
Sensor reading module:

This module take a read from temperature and wheel sensors; save it as
variables, so they can be requested later in the main code.

Also it makes some calculations, in several tools as classes, which can be
called from the main code.

Sensors to use:
    - RPM: A3144 (Replace later with real sensor to be used)
    - Temperature: MLX90614

"""
# Call external libraries/files
import RPi.GPIO as IO
import pigpio
#import Adafruit_GPIO.I2C as I2C
from threading import Thread
import time
import math
import ctypes
#integrals import
from geopy.distance import great_circle
#bluetooth imports
import pexpect
import subprocess
import sys
import re
import datetime

# This variable opens the SkyTraq shared C++ library
lib = ctypes.cdll.LoadLibrary('./lib.so')

#Ctypes type definition of main functions in SkyTraq C++ library
lib.setup_exp.restype=ctypes.c_void_p
lib.loop_exp.restype=ctypes.c_void_p

#Type definition of to-get-variables functions in SkyTraq C++ library
lib.year_exp.restype=ctypes.c_uint
lib.month_exp.restype=ctypes.c_uint
lib.day_exp.restype=ctypes.c_uint
lib.hours_exp.restype=ctypes.c_uint
lib.minutes_exp.restype=ctypes.c_uint
lib.seconds_exp.restype=ctypes.c_double
lib.latitude_exp.restype=ctypes.c_double
lib.longitude_exp.restype=ctypes.c_double
lib.speed_in_mph_exp.restype=ctypes.c_double

#Necessary for setting up the SkyTraq GPS
lib.setup_exp()

#Function necessary to guarantee the I2C operation is not interrupted
#I2C.require_repeated_start()


# Sensors class definition
class Sensors:
    # Rpm variables
    rpm = 0
    mps = 0.00
    mph = 0.00
    dist_miles = 0
    dist_meas = 0.0
    current_dist = 0.0


    elapse = 1
    pulses = 0
    rpm_timer = 0
    # Temperature variables
    temperature = {"tire_C":0.000, "tire_F":0.000, "ambient_C":0.000, "ambient_F":0.000}
    temperature_ref = {"tire_F":0.000, "ambient_F":0.000}


    log_each_mile = 0
    aux_dist = 0.2
    flag_to_measure_dist = False
    #ref_speed = 0
    #ref_pressure = 0
    #ref_inch = 0
    #ref_temp = 0

    switch_mph_reference = False
    mph_reference = 0
    dist_ref = 0
    from_seconds_to_hours_gps = 0
    list_mph = []
    list_latitude = []
    list_longitude = []
    gps_distance_average = 0
    # for integral test
    my_miles = 0

    rotate = 0
    gps_thread = 0

    race_started = False
    time_parameters = [0]

    new_latitude = 0.0
    new_longitude = 0.0
    last_latitude = 0.0
    last_longitude = 0.0
    gps_measure_first_iteration = False 
    mph_average = 0
    lat_average = 0
    long_average = 0
    gps_rpm = 0.0
    list_distance = []
    lenght_time = 0
    measure_time = 0
    key_gps = False
    check_speed_list = False
    counter_rotations = 0

    pulseResult = 0
    last_ = 0
    lastPulse = 0
    pulseAmount = 0
    tire_rotations_per_mile = 0
    circ_inch = 0

    split_decimal = 0
    whole_num = 0
    decimal_num = 0
    factor = 1
    decimal_factor = 1
    current_decimal_factor = 0
    startReadPulses = False




    def __init__(self, GPIO_MODE, RPM_SENSOR_PIN): #, TEMP_SENSOR_ADDR):
        # Passing parameters to local variables
        self.RPM_SENSOR_PIN = RPM_SENSOR_PIN
        #    self._I2C = I2C.Device(TEMP_SENSOR_ADDR, busnum=1) # Initiates I2C
        pi = pigpio.pi()
        
        # Initial setup for GPIOs
        IO.setwarnings(False)
        IO.setmode(GPIO_MODE)

        #IO.setup(self.RPM_SENSOR_PIN, IO.IN)

        # interrupt: pulse detection from Hall-Effect Sensor
        cb = pi.callback(self.RPM_SENSOR_PIN, pigpio.RISING_EDGE, self.elapse_calc)

        # Interrupt: pulse detection from Hall Effect Sensor
        #IO.add_event_detect(
        #self.RPM_SENSOR_PIN,
        #IO.FALLING,
        #callback = self.elapse_calc,
        #bouncetime = 20 # Alert: maybe it should be added
        #)

    # get the definite integral value 
    #def integral_it(self):
    #    print("Integral result: {}".format(Integral(Sensors.my_miles, (Sensors.t, 0, 5)).doit()))
    #    Sensors.my_miles += 1  # increase miles

    def gps_position(self, gps_present_latitude, gps_present_longitude, gps_past_latitude, gps_past_longitude):
        gps_past = (float(gps_past_latitude), float(gps_past_longitude))
        gps_present = (float(gps_present_latitude), float(gps_present_longitude))
        gps_difference = great_circle(gps_past, gps_present).miles
        gps_difference = gps_difference #* 5280.0
        return gps_difference

    def get_seconds_from_gps(self, t_str):
        h, m, s = t_str.split(":")
        return int(h) * 3600 + int(m) * 60 + round(float(s), 2)


    @staticmethod
    # Function to read hall effect sensor and calculate rpm
    def elapse_calc(gpio, level, tick):
        #print("callback by pigpio")
        if Record.record == True and Sensors.startReadPulses == True:
            Sensors.pulses += 1 # Pulses are an important counter to get the value of the distance recorded approximately
            #Sensors.pulseAmount += 1
            #if Sensors.pulses == 5:
            #    Sensors.counter_rotations += 1
            #    Sensors.pulses = 0              # reset pulses
          #  Sensors.elapse = time.time() - Sensors.rpm_timer # It calculates elapse in seconds from the difference between actual time and last time gotten
            #Sensors.rpm_timer = time.time() # Refresh the reference
        else:
            Sensors.pulseAmount = 0
            #Sensors.pulses = 0 # Reset the counter 
            Sensors.counter_rotations = 0
        #Sensors.elapse = self.get_seconds_from_gps(Record.time_string) - Sensors.rpm_timer #time.time() - Sensors.rpm_timer # It calculates elapse in seconds from the difference between actual time and last time gotten
        #Sensors.rpm_timer = self.get_seconds_from_gps(Record.time_string) #time.time() # Refresh the reference

    #def inch_par(self, TIRE_RADIUS_REF):
    #    TIRE_RADIUS_REF
    #    Record.speed_calc(init_Record, TIRE_RADIUS_REF, TIRE_PRESSURE_REF)   # Call this function with tire radius as parameter

    def checkEqual_list(self, lst):
        return lst[1:] == lst[:-1]

    # Function to calculate MPH once RPM and the Tire size is known
    def speed_calc(self, TIRE_RADIUS_REF, TIRE_PRESSURE_REF):
        
        diff_temp = 0
        PsiSum = 0
        RAD_PERCENTAGE = 0 # Percentage

        # if conditions are matched, race will start and we have to restart each important variables like current pulses, distance traveled, etc
        if ((Record.recording_status_flag == False) and ((Record.flager == 1 and Record.tm > (Record.substracter_time - 1.18)) or (Record.flager == 2 and Record.tm > (Record.substracter_time - 1.18)))):
            #print("start!!!")
            if Record.numLeg == 1 or Record.numLeg == None:
                Sensors.startReadPulses = True
                Sensors.pulses = 0 #Sensors.decimal_num 
                Sensors.pulseAmount = Sensors.decimal_num 
                Sensors.current_decimal_factor = Sensors.whole_num + Sensors.decimal_num
                #Sensors.decimal_factor = Sensors.whole_num + Sensors.decimal_num
                Sensors.dist_meas = 0
                Sensors.counter_rotations = 0
                Record.stop_tm = True
                # Set the actual time as a reference
                Record.start_2_count = self.get_seconds_from_gps(Record.time_string) #- .85 #- .8 #- .95  # .95 
                Record.set_record_time = self.get_seconds_from_gps(Record.time_string)#time.time() #Record.get_sec(Record,Record.time_string) #time.time()
                Record.recording_status_flag = True # It will not refresh the reference record time until record has finished
            elif Record.numLeg == 2 or Record.numLeg != 0:
                #print("other stuff")
                Record.recording_status_flag = True # It will not refresh the reference record time until record has finished
                Sensors.startReadPulses = True
                Record.start_2_count = self.get_seconds_from_gps(Record.time_string) #- .85 #- .8 #- .95  # .95 
                Record.set_record_time = self.get_seconds_from_gps(Record.time_string)#time.time() #Record.get_sec(Record,Record.time_string) #time.time()
        #if Sensors.temperature["tire_F"] > Sensors.temperature_ref["tire_F"]:
        #    diff_temp = Sensors.temperature["tire_F"] - Sensors.temperature_ref["tire_F"] # Take the difference between both
        #    PsiSum = (diff_temp * 1.037) / 10 # To know how much will pressure change regarding temperature value
        #    TIRE_PRESSURE_REF += PsiSum # Change to approximate value of pressure

            #JUST AS EXAMPLE OF RADIUS CHANGING:
            ##########################################################
        #    RAD_PERCENTAGE = (PsiSum * 5) / (7 * 100)
        #    TIRE_RADIUS_REF += (TIRE_RADIUS_REF * RAD_PERCENTAGE)
            ##########################################################
        #elif Sensors.temperature["tire_F"] < Sensors.temperature_ref["tire_F"]:
        #    diff_temp = Sensors.temperature_ref["tire_F"] - Sensors.temperature["tire_F"] # Take the difference between both
        #    PsiSum = (diff_temp * 1.037) / 10 # To know how much will pressure change regarding temperature value
        #    TIRE_PRESSURE_REF -= PsiSum # Change to approximate value of pressure
            #JUST AS EXAMPLE OF RADIUS CHANGING:
            ##########################################################
        #    RAD_PERCENTAGE = (PsiSum * 5) / (7 * 100)
        #    TIRE_RADIUS_REF += (TIRE_RADIUS_REF * RAD_PERCENTAGE)
            ##########################################################

        # NOTE: ADD MODIFICATIONS TO THE RADIUS REGARDING PRESSURE
        
        # in case mph reference is measured by hall effect sensor 
        if Sensors.switch_mph_reference == False:   
            #if Sensors.elapse != 0: # This condition is to prevent zero division
                
                
            crrnt = Record.starter_time
            current_pulses = Sensors.pulses
                
            if Sensors.race_started == True:
                if (crrnt - Sensors.last_) >= .5:
                    if ((current_pulses - Sensors.lastPulse) >= 0):
                        Sensors.pulseResult = current_pulses - Sensors.lastPulse
                    Sensors.last_ = crrnt
                    Sensors.lastPulse = Sensors.pulses
                Sensors.mph = round((Sensors.pulseResult/.53), 1)
                    #print("first pulse: {}, last pulse {}, quantity of pulses: {} and speed {}".format(current_pulses, Sensors.lastPulse, Sensors.pulseResult, Sensors.mph))
                    #print("speed {}".format(Sensors.mph))
                #Sensors.dist_miles = circ_inch * 0.0000157828283 # Conversion Inch to Miles
                
                
                #Sensors.rpm = 1 / Sensors.elapse * 60 # Calculates RPM
                #Sensors.rpm = round(Sensors.rpm, 2) # Rounded 2 decimals
                
                #Sensors.mps = Sensors.dist_miles / Sensors.elapse # Calculate Miles per Seconds (MPS)
            
                #Sensors.mph = Sensors.mps * 3600 # Then from MPS to MPH
                #Sensors.mph = round(Sensors.mph, 1) # Rounded 2 decimals
                #Sensors.mph = round(float(Sensors.mph), 1)
                #Sensors.dist_meas = Sensors.dist_miles * Sensors.counter_rotations #Sensors.pulses #Calculates distances measured in Miles
                
                #Sensors.dist_meas = round(Sensors.dist_meas, 2) # Rounded 2 decimals
                #print("Sensors MPH: {}".format(Sensors.mph))
        
        else:   # In case mph reference is measured by the GPS module
            #circ_inch = (2 * TIRE_RADIUS_REF) * math.pi # Calculate wheel circunsference in Inch
            #Sensors.dist_miles = circ_inch * 0.0000157828283 # Conversion Inch to Miles

            #Sensors.rpm = 1 / Sensors.elapse * 60 # Calculates RPM
            #Sensors.rpm = round(Sensors.rpm, 2) # Rounded 2 decimals

            #Sensors.mps = Sensors.dist_miles / Sensors.elapse # Calculate Miles per Seconds (MPS)

            #Sensors.mph = Sensors.mps * 3600 # Then from MPS to MPH
            #Sensors.mph = round(Sensors.mph, 2) # Rounded 2 decimals

            #if len(Sensors.list_time) == 0:
            #    Sensors.list_time.append(Sensors.from_seconds_to_hours_gps)
            #else:
            #    if Sensors.list_time[-1] != Sensors.from_seconds_to_hours_gps:
            #        time = Sensors.from_seconds_to_hours_gps - Sensors.list_time[-1] 

            # fill lists
            

            ## record every 10 seconds
            #if Sensors.race_started == True:
            #    if Sensors.key_gps == False:
            #        Sensors.measure_time = Record.starter_time
            #        Sensors.key_gps = True
            #    print("value of {}".format(Record.starter_time - Sensors.measure_time))
            #    if (Record.starter_time - Sensors.measure_time >= 10):
            #        print("done! ")
            #        Sensors.measure_time = 0
            #        Sensors.key_gps = False
            #    #    print("value of {}".format(Record.starter_time - Sensors.measure_time))
            #    #    #Sensors.measure_time = 
            
            # get current MPH NOTE: FIX the decimals value
            # list mph works to save the higher value achieved for the mph 
            #print("measuring mph by gps")
            #circ_inch = (2 * TIRE_RADIUS_REF) * math.pi # Calculate wheel circunsference in Inch
            Sensors.mph = round(GPS.speed_in_mph, 2) #int(Sensors.mph)
            #Sensors.mps = Sensors.mph/float(3600) # convert miles per hour to miles per second
            #Sensors.dist_miles = Sensors.mps * Record.starter_time
            #Sensors.mps = Sensors.mph/float(3600) # convert miles per hour to miles per second
            #if Sensors.race_started == True:
            #    print("seconds restarted time: {} seconds".format(Record.starter_time))
            #    Sensors.dist_miles = Sensors.mps  * Record.starter_time
            #    Sensors.dist_meas += round(Sensors.dist_miles, 2)
            
            #Sensors.new_latitude = GPS.latitude
            #Sensors.new_longitude = GPS.longitude
            # mph average task if needed 
            #if len(Sensors.list_mph) < 5: # if list size is less than 15 elements
            #    Sensors.list_mph.append(round(GPS.speed_in_mph, 2))
            #elif len(Sensors.list_mph) == 5:
            #    print(" i did it ")
            #    print("list mph: {}".format(Sensors.list_mph))
            #    Sensors.mph_average = round(float(sum(Sensors.list_mph)) / len(Sensors.list_mph), 2)
            #    if Sensors.mph_average > 1:
            #        
            #    del Sensors.list_mph[:]
            #if Sensors.check_speed_list == True:

            #if self.checkEqual_list(Sensors.list_mph) == False: # if car is definitely moving
            if Sensors.race_started == True:
                if Sensors.mph_average >= 5:  # if car is registers an average of 5 
                    Sensors.new_latitude = GPS.latitude
                    Sensors.new_longitude = GPS.longitude
                    if Sensors.new_latitude != Sensors.last_latitude or Sensors.new_longitude != Sensors.last_longitude:
                        if Sensors.gps_measure_first_iteration == False:
                            Sensors.last_latitude = Sensors.new_latitude
                            Sensors.last_longitude = Sensors.new_longitude
                            Sensors.gps_measure_first_iteration = True
                        else:
                            if len(Sensors.list_distance) < 5:
                                distance_av = self.gps_position(Sensors.new_latitude, Sensors.new_longitude, Sensors.last_latitude, Sensors.last_longitude) 
                                Sensors.list_distance.append(distance_av)
                            elif len(Sensors.list_distance) == 5: 
                                Sensors.gps_distance_average = round(float(sum(Sensors.list_distance)) / len(Sensors.list_distance), 2)
                                if Sensors.gps_distance_average >= 0.0032:
                                    Sensors.dist_meas = Sensors.dist_meas + distance_av
                                    Sensors.dist_meas = round(Sensors.dist_meas, 2)
                                print("average: {}".format(Sensors.gps_distance_average))
                                print("distance travel: {}".format(Sensors.dist_meas))
                                Sensors.last_latitude = Sensors.new_latitude
                                Sensors.last_longitude = Sensors.new_longitude
                        #print("")
                        #print("distance between: {}".format(self.gps_position(Sensors.new_latitude, Sensors.new_longitude, Sensors.last_latitude, Sensors.last_longitude)))
                        #print("")

            #print("NEW latitude: {}".format(Sensors.new_latitude))
            #print("NEW longitude: {}".format(Sensors.new_longitude))
            #print("")
            #print("OLD latitude: {}".format(Sensors.last_latitude))
            #print("OLD longitude: {}".format(Sensors.last_longitude))
            #print("")

            #print("")
            #print("distacen between: {}".format())
            #print("")

            #def gps_position(self, gps_present_latitude, gps_present_longitude, gps_past_latitude, gps_past_longitude):
            
            #if Sensors.race_started == True:
                
                #fts = TIRE_RADIUS_REF / 12 # convert inches to feet
                #revol_per_mile = 63360 / TIRE_RADIUS_REF # Get revolutions per mile 
                ##Sensors.rpm = (GPS.speed_in_mph * 5280) / (60 * fts * 2 * math.pi)#1 / Sensors.elapse * 60 # Calculates RPM
                #Sensors.rpm = (47.22 * 5280) / (60 * 17 * 2 * math.pi)#1 / Sensors.elapse * 60 # Calculates RPM
                #Sensors.rpm = round(Sensors.rpm, 3) # Rounded 2 decimals
                #Sensors.dist_miles = Sensors.dist_miles + Sensors.rpm
                #Sensors.dist_meas = Sensors.dist_miles * TIRE_RADIUS_REF
                #print("RPM: {}".format(Sensors.rpm))
                #print("dist measured: {}".format(Sensors.dist_meas))
                #print("time elapsed: {}".format(Record.starter_time))


                # mph average task if needed 
                #if len(Sensors.list_mph) < 5: # if list size is less than 15 elements
                #    Sensors.list_mph.append(round(GPS.speed_in_mph, 2))
                #elif len(Sensors.list_mph) == 5:
                #    #print(" i did it ")
                #    Sensors.mph_average = round(float(sum(Sensors.list_mph)) / len(Sensors.list_mph), 2)
                #    del Sensors.list_mph[:]
                #print("mph_list {}".format(Sensors.list_mph))
                #print("average: {}".format(Sensors.mph_average))
            # CODE TO GET DISTANCE TRAVELED BY GPS DATA LATITUDE AND LONGITUDE
            #if Sensors.race_started == True:
            #    if GPS.speed_in_mph > 0:
            #        print(GPS.speed_in_mph)
            #    if Sensors.new_latitude != Sensors.last_latitude or Sensors.new_longitude != Sensors.last_longitude:
            #        if Sensors.gps_measure_first_iteration == False:
            #            Sensors.last_latitude = Sensors.new_latitude
            #            Sensors.last_longitude = Sensors.new_longitude
            #            Sensors.gps_measure_first_iteration = True
            #        else:
            #            #if self.gps_position(Sensors.new_latitude, Sensors.new_longitude, Sensors.last_latitude, Sensors.last_longitude) > 0:
            #                #print("")
            #                #print("distance between: new data and old data is {}".format(self.gps_position(Sensors.new_latitude, Sensors.new_longitude, Sensors.last_latitude, Sensors.last_longitude)))
            #                #print("")   
#
            #            Sensors.dist_meas = Sensors.dist_meas + self.gps_position(Sensors.new_latitude, Sensors.new_longitude, Sensors.last_latitude, Sensors.last_longitude)
            #            Sensors.dist_meas = round(Sensors.dist_meas, 2)
            #            Sensors.last_latitude = Sensors.new_latitude
            #            Sensors.last_longitude = Sensors.new_longitude
                        #print("")
                        #print("distance between: {}".format(self.gps_position(Sensors.new_latitude, Sensors.new_longitude, Sensors.last_latitude, Sensors.last_longitude)))
                        #print("")

                
                        #if self.gps_position(Sensors.new_latitude, Sensors.new_longitude, Sensors.last_latitude, Sensors.last_longitude) > 0:
                        #    print("")
                        #    print("distance between: new data and old data is {}".format(self.gps_position(Sensors.new_latitude, Sensors.new_longitude, Sensors.last_latitude, Sensors.last_longitude)))
                        #    print("")            
            
            #print("distance traveled by hardcoded time: {} miles".format(Sensors.dist_meas))
            #print("seconds restarted time: {} seconds".format(Record.starter_time))
            #print("time record: {}".format(Record.starter_time))
            #####if Sensors.race_started == True:
            #####    # if size of time parameters list is less than 2, add the element to the list
            #####    #print("array {}".format(Sensors.time_parameters))
            #####    if len(Sensors.time_parameters) < 2:
            #####        Sensors.time_parameters.append(Record.starter_time)
            #####        if len(Sensors.time_parameters) == 2:
            #####            Sensors.dist_miles = round(Integral(Sensors.mps, (Sensors.t, Sensors.time_parameters[0], Sensors.time_parameters[1])).doit(), 2)
            #####            Sensors.dist_meas += Sensors.dist_miles
            #####            print("integral result = {}".format(Integral(Sensors.mps, (Sensors.t, Sensors.time_parameters[0], Sensors.time_parameters[1])).doit()))
            #####            print("Distance traveled from the first time readings: {}".format(Sensors.dist_meas))
            #####            print("dist miles {}".format(Sensors.dist_miles))
            #####            #print("Distance traveled from the first time readings: {}".format(Integral(Sensors.mps, (Sensors.t, Sensors.time_parameters[0], Sensors.time_parameters[1]))))
            #####            #print("test integral: {}".format(Integral(Sensors.my_miles, (Sensors.t, 0, 5)).doit()))
            #####        #print("time parameters list: {}".format(Sensors.time_parameters))
            #####    else:
            #####        # take last element and saved in the first one
            #####        Sensors.time_parameters[0] = Sensors.time_parameters[1]
            #####        Sensors.time_parameters[1] = Record.starter_time
            #####        Sensors.dist_miles = round(Integral(Sensors.mps, (Sensors.t, Sensors.time_parameters[0], Sensors.time_parameters[1])).doit(), 2)
            #####        Sensors.dist_meas += Sensors.dist_miles
            #####        print("integral result = {}".format(Integral(Sensors.mps, (Sensors.t, Sensors.time_parameters[0], Sensors.time_parameters[1])).doit()))
            #####        print("Distance traveled: {}".format(Sensors.dist_meas))
            #####        print("dist miles {}".format(Sensors.dist_miles))
            #####        #print("test integral: {}".format(Integral(Sensors.my_miles, (Sensors.t, 0, 5)).doit()))
            #if Sensors.mph >= 0: # if miles per hour are detected by the system
            #    if len(Sensors.list_mph) == 0:  # if list mph does not have any value
            #        Sensors.list_mph.append(Sensors.mph)    # add the new value of MPH
            #    else:                           # if the suze if list mph is higher
            #        if Sensors.list_mph[-1] >= Sensors.mph: # check if that value is higher than current MPH
            #            Sensors.dist_meas = Sensors.list_mph[-1] * Sensors.from_seconds_to_hours_gps # Calculate distance measured #Sensors.dist_miles * Sensors.pulses #Calculates distances measured in Miles
            #            Sensors.dist_meas = round(Sensors.dist_meas, 2) # Rounded 2 decimals    # round it by 2 decimals 
            #        else:
            #            Sensors.list_mph[-1] = Sensors.mph # set the current mph as the high value achieved, since is higher than list mph

            #last_time = Sensors.from_seconds_to_hours_gps
            #time = 
            

    # Function to read temperature of tires from the IR temperature sensor
    #def temperature_read(self):
        #Sensors.temperature["tire_C"] = self._I2C.readS16(0x07) # Get temperature of the object in Celsius
    #    Sensors.temperature["tire_C"] = (Sensors.temperature["tire_C"] * 0.02) - 273.15
    #    Sensors.temperature["tire_F"] = (Sensors.temperature["tire_C"] * 1.8) + 32 # Convert it to Fahrenheits

        #Sensors.temperature["ambient_C"] = self._I2C.readS16(0x06) # Get temperature of the object in Celsius
    #    Sensors.temperature["ambient_C"] = (Sensors.temperature["ambient_C"] * 0.02) - 273.15
    #    Sensors.temperature["ambient_F"] = (Sensors.temperature["ambient_C"] * 1.8) + 32 # Convert it to Fahrenheits

    # Set the temperature of reference
    #def set_temperature_ref(self):
    #    self.temperature_read()
    #    Sensors.temperature_ref["tire_F"] = Sensors.temperature["tire_F"]
    #    Sensors.temperature_ref["ambient_F"] = Sensors.temperature["ambient_F"]


# Record class definition
class Record:
    record = False
    recording_status_flag = False
    toggle_status_flag = False
    set_record_time = 0.001
    recorded_time = {"hours":0, "minutes":0, "seconds":0}
    t = 0.000
    toggle_status = 2
    last_toggle_time = 0.000
    toggle_button_time = 0
    mph_accurate = 0.0
    general_purpose = 2
    the_time = 0
    stop_tm = False

    gps_reference = 0
    starter_switch = 0
    substracter_time = 0
    starter_time = 0
    sw_time = 5 # 5 seconds predetermined (30 seconds)
    compare_time = 0
    my_difference = 0
    flager = 0
    done = 0
    tm = 0
    last_time_gps = 0
    reverse_count = 0
    current_switch_time = 0
    start_race = 0

    clear_flag = 2
    the_start = 0
    the_end = 0
    flag_go = 0

    result_time = 0
    clear_timer = 0

    seconds_from_gps = 0

    # green leds
    green1_led = 10
    green2_led = 22
    green3_led = 27
    green4_led = 17
    green5_led = 16

    # yellow led
    yellow_led = 9

    # red leds
    red1_led = 19
    red2_led = 13
    red3_led = 6
    red4_led = 11
    red5_led = 18
    gps_working = 25

    switch_timer = 20#12
    time_string = 0
    time_2_compare = 0
    start_2_count = 0

    real_time = 0
    elapsed_time = 0

    numLeg = 0
    end1StLeg = 0

    rst_time_lock = False
    dont_change_switch_opt = False
    disablePulseMeas = False

    #for gps testing
    ##############################################################
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
    min_time_result = 0
    min_time_last = time.time()

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

    gps_bool_change = True 

    # handle gps status
    gps_status = True
    gps_status_ok = False 

    # collect the gps data (coordinates) from spreadsheet data
    coords_a_x = 0
    coords_a_y = 0
    coords_b_x = 0
    coords_b_y = 0

        ##################################

    def __init__(self):
        self.toggle_button = 23 # Red - Arming button
        self.reset_button = 24  # Blue - Clear data (needs to be pushed for n seconds)
        self.reset_timer = 8    #26 # Green - reset timer button
        self.reset_gps = 4      # white - reset gps data
        self.switch_timer = 20#7#12 # switch selector 1min/30sec
        self.gps_working = 25   # Red LED indicator
        self.shutdown_button = 7  # shutdown button
        #self.gps_interrupt = 5      # for testing - gps interrupt value changed

        try:
            # BCM board selected
            IO.setmode(IO.BCM)

            # switch timer input

            # gps working led
            IO.setup(Record.gps_working, IO.OUT)

            # Setting green, yellow and red leds as outputs
            # green leds
            IO.setup(Record.green1_led, IO.OUT)
            IO.setup(Record.green2_led, IO.OUT)
            IO.setup(Record.green3_led, IO.OUT)
            IO.setup(Record.green4_led, IO.OUT)
            IO.setup(Record.green5_led, IO.OUT)

            # yellow led
            IO.setup(Record.yellow_led, IO.OUT)

            # red leds
            IO.setup(Record.red1_led, IO.OUT)
            IO.setup(Record.red2_led, IO.OUT)
            IO.setup(Record.red3_led, IO.OUT)
            IO.setup(Record.red4_led, IO.OUT)
            IO.setup(Record.red5_led, IO.OUT)


            # Setting 4 & 23 as inputs
            IO.setup(self.toggle_button, IO.IN, pull_up_down = IO.PUD_UP)
            IO.setup(self.reset_button, IO.IN, pull_up_down = IO.PUD_UP)
            IO.setup(self.reset_timer, IO.IN, pull_up_down = IO.PUD_UP)
            IO.setup(self.reset_gps, IO.IN, pull_up_down = IO.PUD_UP)
            IO.setup(self.shutdown_button, IO.IN, pull_up_down = IO.PUD_UP) # 5 button as interrupt input 
            IO.setup(Record.switch_timer, IO.IN, pull_up_down = IO.PUD_DOWN)
            #IO.setup(self.gps_interrupt, IO.IN, pull_up_down = IO.PUD_UP)  # GPIO 5 as interrupt input                 

            # Setting 4 & 23 as interrupts
            IO.add_event_detect(self.toggle_button, IO.FALLING, callback = self.toggle_timer, bouncetime = 300)
            IO.add_event_detect(self.reset_button, IO.BOTH, callback = self.clear_all, bouncetime = 50)
            IO.add_event_detect(self.reset_timer, IO.FALLING, callback = self.clear_timer_button, bouncetime = 20)
            IO.add_event_detect(self.reset_gps, IO.FALLING, callback = self.clear_gps, bouncetime = 20)
            IO.add_event_detect(self.shutdown_button, IO.FALLING, callback = self.shutdown_system, bouncetime = 20)
            #IO.add_event_detect(self.gps_interrupt, IO.FALLING, callback = self.change_gps_ref, bouncetime = 20)

        except KeyboardInterrupt:
            IO.cleanup()
            sys.exit

    def change_gps_ref(self, channel):
        #print("accurate!!")
        Record.gps_bool_change = not Record.gps_bool_change
        if Record.gps_bool_change == True and Record.gps_status == True:
            # save gps data   
            Record.h_gps = str(gps.hours)
            Record.m_gps = str(gps.minutes)
            Record.s_gps = str(gps.seconds)
        elif Record.gps_bool_change == False and Record.gps_status == True:
            Record.h_gps = str(Record.wh)
            Record.m_gps = str(Record.wm)
            Record.s_gps = str(record.ws)

    def shutdown_system(self, channel):
        print("pressing shutdown button!!!")

        def go_to_sleep():
            time.sleep(2)
            subprocess.call("sudo shutdown -h now", shell = True)
        t = Thread(target=go_to_sleep)
        t.start()
        print("shutting down system")

    # Function to set the boolean record variable to True or False
    def set_record(self, SET_VALUE_RECORD):
        self.SET_VALUE_RECORD = SET_VALUE_RECORD
        if (self.SET_VALUE_RECORD and Record.toggle_status_flag == False):
            Record.last_toggle_time = Record.time_string #time.time()
        Record.toggle_status_flag = True

    def toggle_timer(self, channel):
        if Record.clear_timer == 0:
            if Record.toggle_status == 1:
                #Record.the_time = GPS.seconds #time.time()
                #Record.time_string = str(GPS.hours) + ":" + str(GPS.minutes) + ":" + str(int(GPS.seconds))
                #Record.time_2_compare = str(GPS.hours) + ":" + str(GPS.minutes) + ":" + str(GPS.seconds)
                #print("get_sec {}".format(record.get_sec(init_record, record.time_string)))
                #Record.the_time = self.get_sec(Record.time_2_compare)
                Record.the_time = self.get_sec(Record.time_string)
                Record.seconds_from_gps = GPS.seconds
                Record.toggle_status = 0
                Record.clear_timer = 1
                Record.starter_switch = 1
                Record.disablePulseMeas = True
                #Sensors.startReadPulses = True 
            else:
                #Record.the_time = GPS.seconds  # time.time()
                #Record.time_string = str(GPS.hours) + ":" + str(GPS.minutes) + ":" + str(int(GPS.seconds))
                #Record.time_2_compare = str(GPS.hours) + ":" + str(GPS.minutes) + ":" + str(GPS.seconds)
                #Record.the_time = self.get_sec(Record.time_2_compare)
                Record.the_time = self.get_sec(Record.time_string)
                Record.seconds_from_gps = GPS.seconds
                Record.toggle_status = 1
                Record.clear_timer = 1
                Record.starter_switch = 2
                Record.disablePulseMeas = True
                #Sensors.startReadPulses = True 

    def timer_switch(self):
        in_state = IO.input(Record.switch_timer)
        if Record.dont_change_switch_opt == False:
            if in_state == True:
                Record.sw_time = 30
                Record.flager = 1
                Record.current_switch_time = "30 Secs"
            else:
                Record.sw_time = 60
                Record.flager = 2
                Record.current_switch_time = "1 Min"

    def str2secs(self, s):
        h, m, s = map(float, s.split(':'))
        return h*3600 + m*60 + s
    
    def get_sec(self, time_str):
        h, m, s = time_str.split(":")
        Record.elapsed_time = int(h) * 3600 + int(m) * 60
        return int(h) * 3600 + int(m) * 60 + float(s)

    def get_time(self, t):
        h, m, s = t.split(":")
        Record.elapsed_time = int(h) * 3600 + int(m) * 60
        return int(h) * 3600 + int(m) * 60 + float(s)

    def the_time_comparison(data, data2):
        data = round((str2secs(data2) - str2secs(data)), 3)

    def counting_up(self, start_sec):
        Record.recorded_time["seconds"] = start_sec
        Record.recorded_time["hours"], Record.recorded_time["seconds"] =  Record.recorded_time["seconds"] // 3600, Record.recorded_time["seconds"] % 3600
        Record.recorded_time["minutes"], Record.recorded_time["seconds"] = Record.recorded_time["seconds"] // 60, Record.recorded_time["seconds"] % 60
        timer_2_show = str(int(Record.recorded_time["hours"])) + ":" + str(int(Record.recorded_time["minutes"])) + ":" + str(round(Record.recorded_time["seconds"], 2))
        return timer_2_show
    
    def splitter(self, seconds2split):
        s = seconds2split.split(".")
        return s[0]
        #print("f {}".format(s[0]))
        
    def start_record(self):
        #self.accurate_speed_calc()
        if(Record.clear_timer == 1):
            if(Record.toggle_status == 0):
                if(self.SET_VALUE_RECORD == True):
                    
                    Record.record = self.SET_VALUE_RECORD # set record var to True
                    #if(Sensors.pulses >= 1): # If car started to move
                    # wait 5 seconds
                    #print("happening A")
                    if(Record.flager == 1):
                        #print("happening B")
                        #Record.compare_time = round(Record.the_time + Record.sw_time)
                        
                        #Record.time_string = str(GPS.hours) + ":" + str(GPS.minutes) + ":" + str(int(GPS.seconds))
                        Record.compare_time = Record.the_time + Record.substracter_time
                        Record.my_difference = Record.compare_time - self.get_sec(Record.time_string) # GPS.seconds)#time.time())
                        # GPS.seconds)#time.time())
                        #Record.tm = round(self.get_sec(Record.time_string) - Record.the_time)
                        Record.tm = Record.the_time - self.get_sec(Record.time_string) + 1
                        Record.tm = -Record.tm
                        Record.reverse_count = Record.the_time - self.get_sec(Record.time_string) # GPS.seconds)#time.time())
                        #print("my_difference: {}".format( Record.my_difference))
                        #print("time: {}".format(Record.tm))
                        
                        if(Record.my_difference <= 0 and Record.recording_status_flag == True):
                            #print("DONE!")
                            ## test!    
                            self.splitter(str(GPS.seconds))
                            #print("result: {}".format(self.get_sec(Record.time_string) - Record.start_2_count))
                            Record.real_time = self.counting_up((self.get_sec(Record.time_string) - Record.start_2_count))
                            self.record_race(Record.set_record_time) # 30 seconds is elapsed
                            Record.flag_go = 1
                            #print("5 seconds elapsed")
                    elif(Record.flager == 2):
                        #print("happening C")
                        #Record.compare_time = round(Record.the_time + Record.sw_time)
                        
                        Record.compare_time = Record.the_time + Record.substracter_time
                        Record.my_difference = Record.compare_time - self.get_sec(Record.time_string) #GPS.seconds)  # time.time())
                        #Record.tm = round(Record.the_time - self.get_sec(Record.time_string)) #GPS.seconds)  # time.time())
                        #Record.tm = round(self.get_sec(Record.time_string) - Record.the_time)
                        Record.tm = Record.the_time - self.get_sec(Record.time_string) + 1
                        Record.tm = -Record.tm
                        #print("elapsed time for 1min: {}".format(Record.tm))
                        #print("my_difference: {}".format(Record.my_difference))
                        #print("time: {}".format(Record.tm))
                        if(Record.my_difference <= 0 and Record.recording_status_flag == True):
                            ## test!
                            self.splitter(str(GPS.seconds))
                            #print("result: {}".format(self.get_sec(Record.time_string) - Record.start_2_count))
                            Record.real_time = self.counting_up((self.get_sec(Record.time_string) - Record.start_2_count))
                            self.record_race(Record.set_record_time) # 30 seconds is elapsed
                            Record.flag_go = 1
                            #print("10 seconds elapsed")
                else:
                    Record.Record = False


            if(Record.toggle_status == 1):
                if(self.SET_VALUE_RECORD == True):
                    Record.record = self.SET_VALUE_RECORD # set record var to True
                    #if(Sensors.pulses >= 1): # If car started to move
                    # wait 5 seconds
                    #print("happening 1")
                    if(Record.flager == 1):
                        #Record.compare_time = round(Record.the_time + Record.sw_time)
                        Record.compare_time = Record.the_time + Record.substracter_time
                        # GPS.seconds)#time.time())
                        Record.my_difference = Record.compare_time - self.get_sec(Record.time_string)
                        # time.time())
                        #Record.my_difference = round(self.get_sec(Record.time_string) - Record.compare_time)
                        Record.tm = Record.the_time - self.get_sec(Record.time_string) + 1  #GPS.seconds)  # time.time())
                        Record.tm = -Record.tm
                        #print("my_difference: {}".format(Record.my_difference))

                        if(Record.my_difference <= 0 and Record.recording_status_flag == True):

                            self.splitter(str(GPS.seconds))
                            ## test!
                            #print("result: {}".format(self.get_sec(Record.time_string) - Record.start_2_count))
                            Record.real_time = self.counting_up((self.get_sec(Record.time_string) - Record.start_2_count))
                            self.record_race(Record.set_record_time) # 30 seconds is elapsed
                            Record.flag_go = 1
                    # wait 10 seconds
                    elif(Record.flager == 2):
                        Record.compare_time = Record.the_time + Record.substracter_time
                        Record.my_difference = Record.compare_time - self.get_sec(Record.time_string)
                        Record.tm = Record.the_time - self.get_sec(Record.time_string) + 1
                        Record.tm = -Record.tm
                        if(Record.my_difference <= 0 and Record.recording_status_flag == True):
                            self.splitter(str(GPS.seconds))
                            Record.real_time = self.counting_up((self.get_sec(Record.time_string) - Record.start_2_count))
                            self.record_race(Record.set_record_time)
                            Record.flag_go = 1 # 30 seconds is elapsed
                else:
                    Record.Record = False

    def record_race(self, set_record_time):
        # time.time() - set_record_time # It calculates elapse in seconds from the difference between actual time and last time gotten
        Record.t = self.get_sec(Record.time_string) - set_record_time
        Record.recorded_time["seconds"] = round(Record.t, 3) # Rounded 3 decimals

        # From seconds we get minutes and hours
        if Record.recorded_time["seconds"] >= 60:
            Record.set_record_time = self.get_sec(Record.time_string)# time.time()
            Record.recorded_time["minutes"] += 1
            if Record.recorded_time["minutes"] > 59:
                Record.recorded_time["minutes"] = 0
                Record.recorded_time["hours"] += 1

    def accurate_speed_calc(self):
        Record.mph_accurate = (GPS.speed_in_mph * 0.6) + (Sensors.mph * 0.4)


   # Function to clear all variables, once Record system has stopped
    # wait for n seconds to clear data 
    def clear_all(self, channel):
        #Sensors.pulses = 0
        #Routes.counter = 0.0
        #Sensors.dist_meas = 0.0
        #Routes.last_dist_meas = 0.0
        #Record.general_purpose = 0
        #del Routes.waypoint_mph[:]
        #del Routes.waypoint_dist_meas[:]
        #del Routes.waypoint_counter[:]
    
        if (IO.input(self.reset_button) == 0):

            Record.the_start = self.get_sec(Record.time_string) #int(Record.time_string) #time.time()
            Record.clear_flag = 1

            print("let's see how long is pressed the button...")
        if (IO.input(self.reset_button) == 1):
            Record.the_end = self.get_sec(Record.time_string) # int(Record.time_string) #time.time()
            Record.clear_flag = 0
            elapsed_in = Record.the_end - Record.the_start
            print("button was pushed through {} seconds".format(elapsed_in))

        return True

    def clear_timer_button(self, channel):
        #if(Record.rst_time_lock == False):
        if(Record.rst_time_lock == False):
            #Record.rst_time_lock = False
            #Record.recorded_time = 0.000
            Record.dont_change_switch_opt = False
            Record.tm = 0
            Record.last_time_gps = 0
            Record.reverse_count = 0
            Record.record = False
            Record.recording_status_flag = False
            Record.toggle_status_flag = False
            Record.t = 0
            Record.recorded_time["seconds"] = 0.000
            Record.recorded_time["minutes"] = 0
            Record.recorded_time["hours"] = 0
            Record.clear_timer = 0
            Record.set_record_time = 0.001
            Record.toggle_button_time = 0.0
            Record.gps_reference = 0
            Record.starter_switch = 0
            Record.substracter_time = int(Record.sw_time)
            Record.tm = 0
            del Routes.waypoint_hours[:]
            del Routes.waypoint_minutes[:]
            del Routes.waypoint_seconds[:]
    


    def clear_gps(self, channel):
        del Routes.waypoint_latitude[:]
        del Routes.waypoint_longitude[:]
        Record.start_race = 0


# GPS class definition
class GPS:
    year = 0
    month = 0
    day = 0
    hours = 0
    minutes = 0
    seconds = 0.000
    latitude = 0.0000000
    longitude = 0.0000000
    speed_in_mph = 0.000

    def setup_skytraq_gps(self):
        lib.setup_exp()

    def update_gnss_data(self):
        # Get NMEA RMC format string data, from SkyTraq GPS by UART serial port
        lib.loop_exp()
        #sleep(0.01) # wait until successful refresh of gnss data (just for security)
        # Get data ready from SkyTraq C++ library
        GPS.year = lib.year_exp()
        GPS.month = lib.month_exp()
        GPS.day = lib.day_exp()
        GPS.hours = lib.hours_exp()
        GPS.minutes = lib.minutes_exp()
        GPS.seconds = lib.seconds_exp()
        GPS.latitude = lib.latitude_exp()
        GPS.longitude = lib.longitude_exp()
        GPS.speed_in_mph = lib.speed_in_mph_exp()

    def update_gps_time(self):
        lib.loop_exp()
        #GPS.hours = lib.hours_exp()
        #GPS.minutes = lib.minutes_exp()
        #GPS.seconds = lib.seconds_exp()


# Routes class definition
class Routes:

    #waypoint = {'mph':0, 'distance measured': 0, 'latitude':0, 'longitude':0, 'hours':0, 'minutes':0, 'seconds':0}
    #waypoint_mph =       []
    waypoint_dist_meas = []
    waypoint_latitude =  []
    waypoint_longitude = []
    waypoint_hours =     []
    waypoint_minutes =   []
    waypoint_seconds =   []
    waypoint_counter =   []
    waypoint_pulses =    []
    waypoint_comparison_data = []
    waypoint_comparison_array = []
    counter = 0
    last_dist_meas = 0.0
    time_complete = []
    time_array = "0"

    #def get_data(self, mph, dist_meas, latitude, longitude, time_hours, time_minutes, time_seconds):
    #def get_data(self, pulses ,mph, dist_meas, latitude, longitude, time_seconds):
    def get_data(self, pulses , dist_meas, latitude, longitude, time_seconds):
        Routes.time_array = time_seconds #str(datetime.timedelta(seconds = time_seconds)) #str(int(time_hours)) + ":" + str(int(time_minutes)) + ":" + str(time_seconds)
        Routes.time_complete.append(Routes.time_array)
        Routes.waypoint_pulses.append(pulses)
        #Routes.time_complete.append(Routes.time_array)
        #Routes.waypoint_mph.append(Sensors.mph)
        Routes.waypoint_dist_meas.append(dist_meas)
        Routes.waypoint_latitude.append(latitude)
        Routes.waypoint_longitude.append(longitude)
        #Routes.waypoint_hours.append(time_hours)
        #Routes.waypoint_minutes.append(time_minutes)
        Routes.waypoint_seconds.append(time_seconds)
        Routes.counter += 1
        Routes.waypoint_counter.append(Routes.counter)
        #Routes.waypoint_comparison_data.append(time_comparison)
        Routes.last_dist_meas = Routes.waypoint_dist_meas[-1] # Save last distance measured
        #print(Routes.waypoint_counter)
        #print("waypoint counter {}".format(Routes.waypoint_counter))
        #print("waypoint mph {}".format(Routes.waypoint_mph))
        #print("waypoint dist meas {}".format(Routes.waypoint_dist_meas))
        #print("waypoint latitude {}".format(Routes.waypoint_latitude))
        #print("waypoint longitude {}".format(Routes.waypoint_longitude))
        #print(" {}".format())
        #print(" {}".format())
        #print(" {}".format())
        #print(" {}".format())

#bluetooth class
# class BluetoothctlError(Exception):
#     """This exception is raised, when bluetoothctl fails to start."""
#     pass


# class Bluetoothctl:
#     """A wrapper for bluetoothctl utility."""
#     data_ble = 0
#     ble_counter = 0

#     def __init__(self):
#         out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
#         self.child = pexpect.spawn("bluetoothctl", echo = False)

#     def get_output(self, command, pause = 0):
#         """Run a command in bluetoothctl prompt, return output as a list of lines."""
#         self.child.send(command + "\n")
#         time.sleep(pause)
#         start_failed = self.child.expect(["bluetooth", pexpect.EOF])

#         if start_failed:
#             raise BluetoothctlError("Bluetoothctl failed after running " + command)

#         return self.child.before.split("\r\n")

#     def start_scan(self):
#         """Start bluetooth scanning process."""
#         try:
#             out = self.get_output("scan on")
#         except BluetoothctlError, e:
#             print(e)
#             return None

#     def make_discoverable(self):
#         """Make device discoverable."""
#         try:
#             out = self.get_output("discoverable on")
#         except BluetoothctlError, e:
#             print(e)
#             return None

#     def parse_device_info(self, info_string):
#         """Parse a string corresponding to a device."""
#         device = {}
#         block_list = ["[\x1b[0;", "removed"]
#         string_valid = not any(keyword in info_string for keyword in block_list)

#         if string_valid:
#             try:
#                 device_position = info_string.index("Device")
#             except ValueError:
#                 pass
#             else:
#                 if device_position > -1:
#                     attribute_list = info_string[device_position:].split(" ", 2)
#                     device = {
#                         "mac_address": attribute_list[1],
#                         "name": attribute_list[2]
#                     }

#         return device

#     def get_available_devices(self):
#         """Return a list of tuples of paired and discoverable devices."""
#         try:
#             out = self.get_output("devices")
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             available_devices = []
#             for line in out:
#                 device = self.parse_device_info(line)
#                 if device:
#                     available_devices.append(device)

#             return available_devices

#     def get_paired_devices(self):
#         """Return a list of tuples of paired devices."""
#         try:
#             out = self.get_output("paired-devices")
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             paired_devices = []
#             for line in out:
#                 device = self.parse_device_info(line)
#                 if device:
#                     paired_devices.append(device)

#             return paired_devices

#     def get_discoverable_devices(self):
#         """Filter paired devices out of available."""
#         available = self.get_available_devices()
#         paired = self.get_paired_devices()

#         return [d for d in available if d not in paired]

#     def get_device_info(self, mac_address):
#         """Get device info by mac address."""
#         try:
#             out = self.get_output("info " + mac_address)
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             return out

#     def get_connectable_devices(self):
#         """Get a  list of connectable devices.
#         Must install 'sudo apt-get install bluez blueztools' to use this"""
#         try:
#             res = []
#             out = subprocess.check_output(["hcitool", "scan"])  # Requires 'apt-get install bluez'
#             out = out.split("\n")
#             device_name_re = re.compile("^\t([0-9,:,A-F]{17})\t(.*)$")
#             for line in out:
#                 device_name = device_name_re.match(line)
#                 if device_name != None:
#                     res.append({
#                             "mac_address": device_name.group(1),
#                             "name": device_name.group(2)
#                         })
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             return res

#     def is_connected(self):
#         """Returns True if there is a current connection to any device, otherwise returns False"""
#         try:
#             res = False
#             out = subprocess.check_output(["hcitool", "con"])  # Requires 'apt-get install bluez'
#             out = out.split("\n")
#             mac_addr_re = re.compile("^.*([0-9,:,A-F]{17}).*$")
#             for line in out:
#                 mac_addr = mac_addr_re.match(line)
#                 if mac_addr != None:
#                     res = True
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             return res

#     def pair(self, mac_address):
#         """Try to pair with a device by mac address."""
#         try:
#             out = self.get_output("pair " + mac_address, 4)
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
#             success = True if res == 1 else False
#             return success

#     def remove(self, mac_address):
#         """Remove paired device by mac address, return success of the operation."""
#         try:
#             out = self.get_output("remove " + mac_address, 3)
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             res = self.child.expect(["not available", "Device has been removed", pexpect.EOF])
#             success = True if res == 1 else False
#             return success

#     def connect(self, mac_address):
#         """Try to connect to a device by mac address."""
#         try:
#             out = self.get_output("connect " + mac_address, 2)
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
#             success = True if res == 1 else False
#             return success

#     def disconnect(self, mac_address):
#         """Try to disconnect to a device by mac address."""
#         try:
#             out = self.get_output("disconnect " + mac_address, 2)
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
#             success = True if res == 1 else False
#             return success

#     def trust(self, mac_address):
#         """Trust the device with the given MAC address"""
#         try:
#             out = self.get_output("trust " + mac_address, 4)
#         except BluetoothctlError, e:
#             print(e)
#             return None
#         else:
#             res = self.child.expect(["not available", "trust succeeded", pexpect.EOF])
#             success = True if res == 1 else False
#             return success

#     def start_agent(self):
#         """Start agent"""
#         try:
#             out = self.get_output("agent on")
#         except BluetoothctlError, e:
#             print(e)
#             return None

#     def default_agent(self):
#         """Start default agent"""
#         try:
#             out = self.get_output("default-agent")
#         except BluetoothctlError, e:
#             print(e)
#             return None
# Datalogger class definition
#class Datalogger:
