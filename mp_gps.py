import multiprocessing as mp 
import Peripherals as peripherals
import time

gps = peripherals.GPS
init_gps = gps()
gps.setup_skytraq_gps(init_gps)

def count_n(v):
    while True:
        gps.update_gnss_data(init_gps)
        v.value = gps.seconds

#if __name__ == '__main__':
v = mp.Value('f', 0.0)
p = mp.Process(target = count_n, args = (v,))
p.start()
#p.join()

while  True:
    print(v.value)
    #time.sleep(.5)
