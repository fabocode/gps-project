# Hall Effect sensor simulation

import RPi.GPIO as IO
import time

hall_effect_sensor = 21
button = 26#20

frequency = 0.5
period = 0.00
timer = time.time()

IO.setwarnings(False) #do not show warnings
IO.setmode(IO.BCM)

IO.setup(hall_effect_sensor, IO.OUT)
IO.setup(button, IO.IN)

IO.output(hall_effect_sensor, IO.HIGH)

def accelerator():
    global timer, frequency, button
    timer = time.time() - timer
    if (IO.input(button) == 0 and timer > 2 and frequency < 70):
       frequency += 5
       timer = time.time()
    if (IO.input(button) == 1 and timer > 2 and frequency >= 5):
       frequency -= 5
       timer = time.time()

try:
    while True:
        if frequency > 0:
            IO.output(hall_effect_sensor, IO.HIGH)
            period = float(1/frequency)
            time.sleep(period)
            IO.output(hall_effect_sensor, IO.LOW)
            time.sleep(period)
        else:
            frequency = 0.1
        accelerator()
finally:
     print("Cleaning up pins...")
     IO.cleanup()
     
