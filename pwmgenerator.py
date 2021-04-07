import pigpio, time

pi = pigpio.pi()    # pi accesses the local Pi's GPIO
pwm_pin = 12#5#21 #13
frq = 800 #24000     # in Hz

try:
    #pi.set_PWM_frequency(pwm_pin, frq)
    while True:
        #pi.set_PWM_dutycycle(pwm_pin, 255)
        pi.hardware_PWM(pwm_pin, frq, 500000)
        time.sleep(1)

except KeyboardInterrupt:
    pi.write(pwm_pin, 0)
    pi.stop()
