import subprocess
import time


counter = 0
#out2 = subprocess.check_output("ls /home/pi/Documents/myRoutes", shell = True)   # Save devices plugged to device into "out"
while True:
    counter += 1
    dirs = []
    out = subprocess.check_output("ls /home/pi/Documents/myRoutes", shell = True)   # Save devices plugged to device into "out"
    sp = out.split(".xlsx")
    for i in range(len(sp)):
        if(sp[i] != '\n'):
            dirs.append(sp[i].strip())
            print(sp[i])
    print("counter: {}".format(counter))
    print("dirs {}".format(dirs))

    #sp = out2.split(".xlsx")
    ##sp = out2.split("/n")
    ##print(sp)
    ##print(len(sp))
    #for i in range(len(sp)):
    #    if(sp[i] != '\n'):
    #        #Main_Screen.listed.append(sp[i])
    #        #print("list {}".format(Main_Screen.listed.append(sp[i])))
    #        print(sp[i])
    time.sleep(1)