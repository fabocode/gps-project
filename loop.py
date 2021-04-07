import time

while True:
    f = open('gps_time.txt', 'r')
    print(f.read())
    f.close()
    time.sleep(2)