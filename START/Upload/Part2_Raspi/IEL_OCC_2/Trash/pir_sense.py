#!/usr/bin/python3.4

import RPi.GPIO as GPIO
import time
import sys

Led = [36,38,40]

Sensor = [11,13,15] #13 is light sensor

def setup():
    #This allows the lights to stay on for multiple passes of the program
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    #initializes the LEDs for output
    for i in Led:
        GPIO.setup(i, GPIO.OUT, initial = 0 )   # Set LedPin's mode is output
        GPIO.output(i, 0) # Set LedPin high(+3.3V) to off led

    #Initializing the sensors
    for i in Sensor:
        GPIO.setup(i, GPIO.IN)

def test():
    for i in Led:
        on(i)
        time.sleep(0.5)
        off(i)

def on(value):
    GPIO.output(value, GPIO.HIGH)

def off(value):
    GPIO.output(value, GPIO.LOW)

def sense(port):
    try:
        state = GPIO.input(Sensor[port])
        if state:
            on(Led[port])
        else:
            off(Led[port])
    except:
        print('Look for errors within sense function')
    return state

def loop():
    state = 2
    try:
        while True:
            print('State{} is: {}'.format(state, sense(state)))
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed
        print("Terminating")
    except:
        print("Check for further problems")
    finally:
        destroy()

def destroy():
    for i in Led:
        off(i)# led off
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':# Program start from here
    setup()
    test()
    loop()
