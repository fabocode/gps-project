import RPi.GPIO as IO          
import time                            #calling time to provide delays in program

pin = 21
freq = 1000
dutycycle = 50

IO.setwarnings(False)           #do not show any warnings
IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as GPIO19)
IO.setup(pin,IO.OUT)           # initialize GPIO19 as an output.

p = IO.PWM(pin,freq)          #GPIO19 as PWM output, with 100Hz frequency
p.start(dutycycle)                              #generate PWM signal with 0% duty cycle

try:
    while 1:                               #execute loop forever
        time.sleep(0.1)
        # for x in range (50):                          #execute loop for 50 times, x being incremented from 0 to 49.
        #     p.ChangeDutyCycle(x)               #change duty cycle for varying the brightness of LED.
        #     time.sleep(0.1)                           #sleep for 100m second
        
        # for x in range (50):                         #execute loop for 50 times, x being incremented from 0 to 49.
        #     p.ChangeDutyCycle(50-x)        #change duty cycle for changing the brightness of LED.
        #     time.sleep(0.1)                          #sleep for 100m second
except KeyboardInterrupt:
    IO.cleanup()

IO.cleanup()
