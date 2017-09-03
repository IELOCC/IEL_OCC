import sys
sys.path.append('./tsl2591')
import sensor
import time

#This is how we define a new sensor in our address system: name = sensor.Sensor(sensor_address)
tsl2591 = sensor.Sensor(0x29)
tsl2561 = sensor.Sensor(0x39)

while True:
    try:
        nine = tsl2591.read_ch0()
        six = tsl2561.read_ch1()
        print("TSL2591 full value: {}\t| \tTSL2561 full value: {}".format(nine,six))
    except KeyboardInterrupt:
        exit()
