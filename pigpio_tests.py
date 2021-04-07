import pigpio, time

pi = pigpio.pi()    # pi accesses the local Pi's GPIO
#led_pi = 13 
input_pulse = 5 #21

pulse_counter = 0

def my_callback(gpio, level, tick):
    global pulse_counter
    pulse_counter += 1

cb = pi.callback(input_pulse, pigpio.RISING_EDGE, my_callback)

try:
    time.sleep(1)
    print("number of pulses in 1 seconds\n{} pulses".format(pulse_counter))

except KeyboardInterrupt:
    #pi.write(led_pi, 0)
    pi.stop()
