import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

pwm = GPIO.PWM(13, 4) # GPIO13, frequency=50Hz
pwm.start(0)

try:
    while True:
        pwm.ChangeDutyCycle(1)
        time.sleep(60)

except KeyboardInterrupt:
   GPIO.cleanup()

pwm.stop()
GPIO.cleanup()
