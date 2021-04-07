from multiprocessing import Process, Queue
import subprocess
import Peripherals as peripherals
import time

gps = peripherals.GPS
init_gps = gps()
gps.setup_skytraq_gps(init_gps)

def queuer(q, key):
    try:
        while key == False:
            gps.update_gnss_data(init_gps) # get gps data
            #print(gps.seconds)
            q.put(gps.seconds)
            #counter += 1
            #q.put(counter)

    except KeyboardInterrupt:
        print("terminated here")
        task = subprocess.Popen('launcher.exe localhost filename.dut', shell=True)
        # some time later
        task.terminate()
        key = True

#counter = 0
key = False
q = Queue()
a = Process(target=queuer, args=(q,key))
a.start()

if __name__ == '__main__':

    try:
        
        while True:
            #item = q.get()
            print "Running", q.get()#item
            #time.sleep(1)
            #if not q.empty():
            #    #item = q.get()
            #    print "Running", item
            ##time.sleep(1)
            #print("sleep")
            #time.sleep(1)
            #    #time.sleep(1)
            #else:
            #    print "No jobs"
            #    #time.sleep(1)
    except KeyboardInterrupt:
        print("terminated")
        task = subprocess.Popen('launcher.exe localhost filename.dut', shell=True)
        # some time later
        task.terminate()
        key = True