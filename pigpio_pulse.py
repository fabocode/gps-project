import time

import pigpio

WIND_GPIO=4

#pigpio.start()

pigpio.set_mode(WIND_GPIO, pigpio.INPUT)
pigpio.set_pull_up_down(WIND_GPIO, pigpio.PUD_UP)

wind_cb = pigpio.callback(WIND_GPIO, pigpio.FALLING_EDGE)

old_count = 0

#while True:
#
#   time.sleep(5)
#
#   count = wind_cb.tally()
#   print("counted {} pulses".format(count - old_count))
#   old_count = count

while True:

   time.sleep(5)

   count = wind_cb.tally()
   print("counted {} pulses".format(count - old_count))
   old_count = count

#pigpio.stop()