####################################################
#   /brief sketch for calculating distance and 
#   intersection between the finish line and the 
#   user. Simulated with time and a list of previously
#
#
####################################################
from time import time 
import geopy.distance
import gpx_parse
from shapely.geometry import LineString

finish_line = {
    'point_a': (11.010726, -74.905604),
    'point_b': (11.011456, -74.899899)
}

# file_path = 'C:\workspace\python\garbage_code\gpx_module\complex_test.gpx'
file_path = '/home/pi/Documents/GPS_TRACKING_SYSTEM/src/test_gpx/complex_test.gpx'
gpx = gpx_parse.gpx_parser(file_path)
locations = gpx.get_gpx_cords()
last_time = time()
index = 0
distance_travel = 0
running = []

while True:

    READ_TIME = 1
    if time() - last_time >= READ_TIME:
        last_time = time()
        cord_list = gpx.get_gpx_cords() # get the gps cords from gpx file 

        # if end of cord_list is reached, end loop
        if index >= len(cord_list):
            print("race ended")
            break

        # assign current gps data to cord
        running.append(cord_list[index]) 

        # if growing list has enough values to compare data 
        #  and is able to calculate distance 
        if len(running) > 1:
            # calculate distance traveled 
            distance_travel = distance_travel + \
                geopy.distance.distance(cord_list[index], 
                    cord_list[index - 1]).km
            # print(f'cords 1: {cord_list[index]} and cords 2: {cord_list[index - 1]} have this distance: {distance_travel}')
            print("cords 1: {} and cords 2: {} have this distance: {}".format(cord_list[index], cord_list[index - 1], distance_travel))
            # check if there's an intersection 
            line1 = LineString([finish_line["point_a"], finish_line["point_b"]])
            line2 = LineString(running)
            if line1.intersects(line2):
                print("there is an intersection!")
                print(line1.intersection(line2))
                break

            else:
                print("no intersection")

        # increment that index!! 
        index += 1

