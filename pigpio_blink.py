import pigpio, time

pi = pigpio.pi()
pi.set_mode(13, pigpio.OUTPUT)

while True:
   pi.write(13,1)
   time.sleep(1)
   pi.write(13,0)
   time.sleep(1)
