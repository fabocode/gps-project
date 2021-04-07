#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO
import time  

counter_pulses = 0

GPIO.setmode(GPIO.BCM)  
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
def my_callback2(channel):  
    global counter_pulses
    counter_pulses += 1
    #print "Rising edge detected on 21" 
 
GPIO.add_event_detect(21, GPIO.RISING, callback=my_callback2, bouncetime=300)  
  
try: 
    time.sleep(60)
    print("amount of pulses in 1 second: \n{} pulses".format(counter_pulses))
    #while True: 
    #    time.sleep(5) 
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
