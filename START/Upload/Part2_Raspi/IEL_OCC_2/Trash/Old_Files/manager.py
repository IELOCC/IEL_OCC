#!/usr/bin/python2.7

import subprocess
import os
import confirm
import write_mac
import status
import functions
import sensor_collection
import datetime

mac='4C:57:CA:78:44:C8'
#Initialization Settings
def initialize():
    #Create an object representing the day
    day = status.Status()
    #Tries to write the mac address if it's not currently set
    try:
        while int(day.get('confirmed')) == 0:
            print "Attempting to write MAC"
            write_mac.write()
            print "Successfully wrote MAC"
            print "Confirming Status"
            day.set('confirmed',int(confirm.status()))
            print day.get('confirmed')
            print "Successfully confirmed status"
    except:
        print "There was an error with the mac address"
    return None

def events():
    events = functions.Functions()
    return None

if __name__=="__main__":
    #initialize()
    thomas = functions.Functions()
    june = functions.Functions()


    while True:
        #print sensor_collection.out()
        thomas.update('4C:57:CA:78:44:C8')#sensor_collection.lux())
        #print 'Thomas: '+str(thomas.new_blue)
        june.update('1C:5C:F2:79:35:56')
        #print 'June: '+str(june.new_blue)
        writing = str(thomas.new_blue)+','+str(june.new_blue)+','+str(datetime.datetime.now())
        with open('Data_Collection/bluetooth_accuracy.csv','a+') as w:
            w.write(writing+'\n')
            w.close()
