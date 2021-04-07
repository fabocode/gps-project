from sympy import Integral, Symbol
import time

t = Symbol('t')
miles = 0 #Symbol('k')

# Indefinite Integral
#print("Integral result: {}".format(Integral(miles, t).doit()))

while True:
    # Definite Integral from 0 to 5 seconds
    print("Integral result: {}".format(Integral(miles, (t, 0, 5)).doit()))
    miles += 1  # increase miles
    time.sleep(.01)