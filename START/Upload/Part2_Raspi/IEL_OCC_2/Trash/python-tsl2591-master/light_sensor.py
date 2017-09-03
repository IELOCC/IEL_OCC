import tsl2591
import sys
import os

tsl = tsl2591.Tsl2591()
looper = True

while looper:
    try:
        full, ir = tsl.get_full_luminosity()
        lux = tsl.calculate_lux(full, ir)
        print("Full: {}\tIR: {}  \tLux: {:.4}".format(full,ir,lux))
    except KeyboardInterrupt:
        looper = False

print("Program Ending")

