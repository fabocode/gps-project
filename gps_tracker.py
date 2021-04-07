# from shapely.geometry import LineString
# A = (11.003370, -74.840933)
# B = (11.003381, -74.838905)

# C = (11.004571, -74.839967)
# D = (11.001938, -74.839774)


# # line1 = LineString([A, (1,0), (1,1)])
# line1 = LineString([A, B])
# line2 = LineString([C, D])

# print(line1.intersection(line2))

from shapely.geometry import LineString
import Peripherals as peripherals
import threading
import time

gps = peripherals.GPS

flag = False


# A = (11.003370, -74.840933)
# B = (11.003381, -74.838905)
## local tests here!
A = (11.007168, -74.835110)
B = (11.006681, -74.834265)


def loop_thread():
    while flag == False:
       #gps.update_gps_time(init_gps)
       gps.update_gnss_data(init_gps)  # get gps data
       #print("gps seconds inside thread: {}".format(gps.seconds))


try:
    init_gps = gps()
    gps.setup_skytraq_gps(init_gps)

    
    my_thread = threading.Thread(target=loop_thread)  # instance the thread
    my_thread.start()   # call to start the thread

    option = raw_input("type 'y' to start: ").lower()

    if option == 'y':

        C = (gps.latitude, gps.longitude)
        # C = (11.005231, -74.834780)
        # C= (11.006415, -74.835486)
        while True:

            line1 = LineString([A, B])
            D = (gps.latitude, gps.longitude)
            #D = 11.006415, -74.835486#
            # D = (11.0055533333, -74.8340316667)
            line2 = LineString([C, D])
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
            #11.006035, -74.83465
            # 11.00594, -74.83467
            # 11.006415, -74.835486 -- new
            if line1.intersects(line2):
                print("there is an intersection!")
                print(line1.intersection(line2))
                break
            else:
                print("no intersection")
            # time.sleep(1)
    else:
        flag = True
        print("no option entered")
        sys.exit


except KeyboardInterrupt:
    flag = True
    # IO.cleanup()
    sys.exit

# A = (11.003370, -74.840933)
# B = (11.003381, -74.838905)

# C = (11.004571, -74.839967)
# D = (11.001938, -74.839774)
# E = (11.004661, -74.838753) # Wrong


# # line1 = LineString([A, (1,0), (1,1)])
# line1 = LineString([A, B])
# line2 = LineString([C, D])


# # print(line1.intersection(line2))
# print(line1.intersects(line2))

# # print(str(line1.intersection(line2)))
# # b = a[25:]
# # a = a[7:24]
# # print(a[7:24])
# # print(len(a))
# # print(type(line1.intersection(line2)))



# A = (11.005855, -74.834667)
# # B = (11.05294, -74.834192)
# B = (11.005344, -74.834031)
# C = (11.005263, -74.834775)
# D = (11.0055533333, -74.8340316667)

# line1 = LineString([A, B])
# line2 = LineString([C, D])

# pr
# print(line1.intersection(line2))
# print(line1.intersects(line2))