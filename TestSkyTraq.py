import ctypes
from time import sleep

lib = ctypes.cdll.LoadLibrary('./lib.so')

#Type definitiion of main functions in C++ library
lib.setup_exp.restype=ctypes.c_void_p
lib.loop_exp.restype=ctypes.c_void_p

#Type definition of to-get-variables functions in C++ library
lib.year_exp.restype=ctypes.c_uint
lib.month_exp.restype=ctypes.c_uint
lib.day_exp.restype=ctypes.c_uint
lib.hours_exp.restype=ctypes.c_uint
lib.minutes_exp.restype=ctypes.c_uint
lib.seconds_exp.restype=ctypes.c_double
lib.latitude_exp.restype=ctypes.c_double
lib.longitude_exp.restype=ctypes.c_double
lib.speed_in_mph_exp.restype=ctypes.c_double

lib.setup_exp()

while 1:
    lib.loop_exp()
    #sleep(0.01)
    
    #Date
    year = lib.year_exp()
    month = lib.month_exp()
    day = lib.day_exp()
    print("Date: {0}/{1}/{2}".format(month, day, year))

    #Time
    hours = lib.hours_exp()
    minutes = lib.minutes_exp()
    seconds = round(lib.seconds_exp(), 4)
    print("Time: {0}:{1}:{2}".format(hours, minutes, seconds))

    #Latitude
    latitude = round(lib.latitude_exp(), 4)
    print("Latitude: {0}".format(latitude))

    #Longitude
    longitude = round(lib.longitude_exp(), 4)
    print("Longitude: {0}".format(longitude))

    #Speed in MPH (Knots converted to MPH in the process)
    speed_in_mph = round(lib.speed_in_mph_exp(), 2)
    print("Speed: {0}-MPH".format(speed_in_mph))
    
    print("Package gotten!!!")