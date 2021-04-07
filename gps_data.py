#import Peripherals as peripherals
#import time
#import RPi.GPIO as IO

import ctypes

# This variable opens the SkyTraq shared C++ library
lib = ctypes.cdll.LoadLibrary('./lib.so')

#Ctypes type definition of main functions in SkyTraq C++ library
lib.setup_exp.restype = ctypes.c_void_p
lib.loop_exp.restype = ctypes.c_void_p

#Type definition of to-get-variables functions in SkyTraq C++ library
lib.year_exp.restype = ctypes.c_uint
lib.month_exp.restype = ctypes.c_uint
lib.day_exp.restype = ctypes.c_uint
lib.hours_exp.restype = ctypes.c_uint
lib.minutes_exp.restype = ctypes.c_uint
lib.seconds_exp.restype = ctypes.c_double
lib.latitude_exp.restype = ctypes.c_double
lib.longitude_exp.restype = ctypes.c_double
lib.speed_in_mph_exp.restype = ctypes.c_double

#Necessary for setting up the SkyTraq GPS
lib.setup_exp()


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
        #GPS.hours = lib.hours_exp()
        #GPS.minutes = lib.minutes_exp()
        #GPS.seconds = lib.seconds_exp()
        GPS.latitude = lib.latitude_exp()
        GPS.longitude = lib.longitude_exp()
        GPS.speed_in_mph = lib.speed_in_mph_exp()

    def update_gps_time(self):
        lib.loop_exp()
        GPS.hours = lib.hours_exp()
        GPS.minutes = lib.minutes_exp()
        GPS.seconds = lib.seconds_exp()


#gps_data = GPS()
#gps = GPS()

#while True:
#    gps.update_gps_time()
#    #print("UTC_TIME: {0}:{1}:{2}".format(gps.hours, gps.minutes, gps.seconds))

