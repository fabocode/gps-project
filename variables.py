import gps_data
import time

gps = gps_data.GPS

# Gps class
init_gps = gps()

# Setup the GPS device
gps.setup_skytraq_gps(init_gps)

h = 0
m = 0
s = 0

gps.update_gnss_data(init_gps)
print(gps.seconds)

#while True:
#    # date, latitude, longitude, etc
#    gps.update_gnss_data(init_gps)
#    
#    # Get NMEA RMC format string data, from SkyTraq GPS by UART serial port
#    #gps.update_gps_time(init_gps)
#
#    #print("GPS Info. ==>> date:{0}/{1}/{2} UTC_time:{3}:{4}:{5} latitude:{6} longitude:{7} speed:{8}-MPH \n".format(
#    #    gps.month,
#    #    gps.day,
#    #    gps.year,
#    #    gps.hours,
#    #    gps.minutes,
#    #    gps.seconds,
#    #    gps.latitude,
#    #    gps.longitude,
#    #    gps.speed_in_mph
#    #))
#
#    h = gps.hours
#    m = gps.minutes
#    s = str(gps.seconds)
#    print('seconds elapsed: {}'. format(s))
#    f = open('gps_time.txt', 'w')
#    f.write(s)
#    f.close()



#x = 5 
#
#while True:
#    x = str(input('input x: '))
#    f = open('x.txt', 'w')
#    f.write(x)
#    f.close()

    
