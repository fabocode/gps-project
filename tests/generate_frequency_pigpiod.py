import pigpio 
import time 
pigpio_duty = 1e6

pin = 21
freq = 400
duty = pigpio_duty * 0.5
pi = pigpio.pi() 

def generate_hardware_pwm(freq, duty):
    pin = 18 # 18 GPIO is hardware capable to generate PWM signals from hardware clock
    # starts a pwm signal with described pin, frequenecy and duty cycle 
    pi.hardware_PWM(pin, freq, duty)

def generate_soft_pwm(pin,freq, dutycycle):
    pin = 21
    duty = 255 * .1 # _range * (percetange of duty cycle ) / 100
    pi.set_PWM_frequency(pin, freq)
    pi.set_PWM_dutycycle(pin, duty)


try: #
    # start pwm 
    generate_soft_pwm(pin, freq, duty)
    # generate_hardware_pwm(freq, duty)
    while True: 
        time.sleep(0.1)
except KeyboardInterrupt:
    # pi.set_PWM_frequency(pin, 0)
    pi.set_PWM_dutycycle(pin, 0)
    pi.stop()

pi.stop()
