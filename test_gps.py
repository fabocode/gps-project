import gps_data
import time

gps = gps_data.GPS

# Gps class
init_gps = gps()

# Setup the GPS device
gps.setup_skytraq_gps(init_gps)


while True:
    # date, latitude, longitude, etc
    gps.update_gnss_data(init_gps)

    # Get NMEA RMC format string data, from SkyTraq GPS by UART serial port
    #gps.update_gps_time(init_gps)
    
    #print("GPS Info. ==>> date:{0}/{1}/{2} UTC_time:{3}:{4}:{5} latitude:{6} longitude:{7} speed:{8}-MPH \n".format(
    #gps.month,
    #gps.day,
    #gps.year,
    #gps.hours,
    #gps.minutes,
    #gps.seconds,
    #gps.latitude,
    #gps.longitude,
    #gps.speed_in_mph
    #))
    time.sleep(.00000001)
    print("UTC_TIME: {0}:{1}:{2}".format(gps.hours, gps.minutes, gps.seconds))
