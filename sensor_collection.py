#!/usr/bin/python2.7
import sys
import os
import subprocess
import re
import time

def initialize():
    try:
        #This is for the C02 Sensor
        import NDIR
        sensor = NDIR.Sensor(0x4D)
        sensor.begin()
    except:
        print "CO2 is down."

    try:
        #For the motion detector
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.IN)
    except:
        print "Motion down."
    return None

#C02
def co2():
    try:
        sensor.measure()
        return sensor.ppm
    except:
        return -1

#TSL2561
def lux():
    try:
        process = subprocess.Popen(["./tsl2561.o"],stdout=subprocess.PIPE)
        out = str(process.communicate()[0]).rstrip("'")
        tsl2561 = [];
        runner = [tsl2561.append(i) for i in out if i.isdigit()]
        return int(''.join(tsl2561))
    except:
        return -1

#Motion Detector
def motion():
    try:
        return int(GPIO.input(11))
    except:
        return -1

def out():
    return [int(co2()),int(lux()),int(motion())]

def main():
    return None

if __name__=="__main__":
    initialize()
    main()
