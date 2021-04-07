import subprocess, glob, os, time



key = False
folder_key = "0"

while True:
    out = subprocess.check_output("df", shell = True)   # Save devices plugged to device into "out"
    if(len(out) >= 570):                                # Check if the string is enoug to know if a drive is connected 
        #if sc_usb == 0:
        splited = out.split(" ")                        # Split the string every space
        for i in range(0, len(splited)):                # iterate the list
            if(len(splited[i]) == 24):                  # if the item of the list is same as target item "sda1" device
                usb_dev = splited[i].split("/")         # split the string every "/"
                for i in range(0, len(usb_dev)):        # iterate current list
                    if(usb_dev[i] == "sda1"):           # if iterated item is sda1
                        #print(" {}".format(usb_dev[i]))
                        check_files = subprocess.check_output("ls /media/pi", shell = True) # save the output of 'ls /media/pi'
                        check_files = check_files.split("\n")                               # removing the "\n"
                        #print("check files review {}".format(check_files))
                        folder = subprocess.check_output("ls /media/pi/" + check_files[0], shell = True) # save the output of 'ls /media/pi'
                        folder = folder.split("\n")   
                        #print("list of files {}".format(folder))
                        for i in range(len(folder)):
                            #print(folder[i])#if folder[i]
                            if folder[i] == "GPS SYSTEM GENERATED ROUTE":
                                print("I found the file {}".format(folder[i]))
                                key = True
                                break
                            #else:
                            #    print("This is not the folder :(")
                                
                        if key == False:
                            key = False
                            folder_create = 'mkdir /media/pi/' + check_files[0] + "/" + "'" + "GPS SYSTEM GENERATED ROUTE" + "'"
                            print("folder doesn't exist, I will create it")
                            print("{}".format(folder_create))
                            subprocess.call(folder_create, shell = True)
                        #else:
                        #    key = False
                        #    folder_create = 'mkdir /media/pi/' + check_files[0] + "/" + "'" + "GPS SYSTEM GENERATED ROUTE" + "'"
                        #    print("folder doesn't exist, I will create it")
                        #    print("{}".format(folder_create))
                        #    subprocess.call(folder_create, shell = True)
                        
                        
                        #if key == True:
                        #    folder_key = folder[i]
                        #    print("folder key = {}".format(folder_key))
                        #else:
                        #    key = False
                        #    folder_create = 'mkdir /media/pi/' + check_files[0] + "/" + "'" + "GPS SYSTEM GENERATED ROUTE" + "'"
                        #    print("folder doesn't exist, I will create it")
                        #    print("{}".format(folder_create))
                        #    subprocess.call(folder_create, shell = True)
                        
                        
                        
                            #print('mkdir /media/pi/' + "{}" + "/" + "GPS SYSTEM GENERATED ROUTE".format(check_files[0]))
                            #create = subprocess.check_output("mkdir /media/pi/" + check_files[0] + "/" + "GPS", shell = True)
                            #subprocess.call('mkdir "/media/pi/' + check_files[0] + "/" +  "GPS SYSTEM GENERATED ROUTE", shell = True)
                        #l = os.chdir("/media/pi/" + check_files[0])                             # take directory as reference
                        #print("list of files {}".format(l))
                        #for file in glob.glob("*.xlsx"):                                     # Iterate each .txt file recognized
                        #    # copy each file in the correspondent directory 
                        #    final = subprocess.check_output(("sudo cp /media/pi/" + check_files[0] + "/" + '"' + file + '"' + "  /home/pi/Documents/LoadRoute"), shell = True)                             
                        #    print("done!")
                        ##sc_usb = 1
                        ##get_time_after_copy = time.time()
                        #print("for loop done!")
    #print()
    else:
        print("none usb detected")
    time.sleep(1)