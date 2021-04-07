import subprocess
import time

list_2 = []

while True:
    list_1 = []
    index = -1

    out = subprocess.check_output("ls /home/pi/Documents/myRoutes", shell = True)   # Save devices plugged to device into "out"
    sp = out.split(".xlsx")
    
    for i in range(len(sp)):
        if(sp[i] != '\n'):
            list_1.append(sp[i].strip())
    if len(list_1) > len(list_2):
        for i in list_1:
            for x in list_2:
                if i == x: #in x:
                    #print("item from list 1 {} is in list 2 {}".format(i, x))
                    break
            else:
                #print("item from list 1 {} is NOT in list 2".format(i))
                list_2.append(i)

    if len(list_1) < len(list_2):
        print("current is smaller ")
        for i in list_2: # list 1
            for x in list_1:    # list 2
                if i == x: #in x: 
                    index += 1
                    #print("item from list 1 {} is in list 2 {} and the index is {}".format(i, x, index))
                    break
            else:
                index += 1
                print("item from list 1 {} is NOT in list 2 and I have to delete it and the index is {}".format(i,index))
                del list_2[index]
    
    print("new {}".format(list_1))
    print("")
    print("old {}".format(list_2))
    print("")
    time.sleep(10)

    