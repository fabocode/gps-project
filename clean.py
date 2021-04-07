import RPi.GPIO as GPIO

clean = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(clean, GPIO.OUT)

GPIO.cleanup()
