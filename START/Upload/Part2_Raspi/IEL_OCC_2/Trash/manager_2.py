#!/usr/bin/python2.7

import subprocess
import os
import confirm
#import write_mac
import status
import functions
import datetime
import time
from Queue import Queue
from threading import Thread

mac='4C:57:CA:78:44:C8'
'''
#Initialization Settings
def initialize():
    #Create an object representing the day
    day = status.Status()
    #Tries to write the mac address if it's not currently set
    try:
        while int(day.get('confirmed')) == 0:
            print "Attempting to write MAC"
            #write_mac.write()
            print "Successfully wrote MAC"
            print "Confirming Status"
            day.set('confirmed',int(confirm.status()))
            print day.get('confirmed')
            print "Successfully confirmed status"
    except:
        print "There was an error with the mac address"
    return None
'''
def events():
    events = functions.Functions()
    return None

def run(minutes):
    #Builds our code to operate for 5 minutes
    start_time = int(time.time())
    end_time = start_time+(60*minutes)

    system = functions.Functions()
    commands = [system.bluetooth,system.switch_sample,system.sensors]

    #Starts my threading list to maintain the integrity of the individual address
    workers = []

    #Starts the multithreading
    workers.append(Thread(target=commands[0]))
    workers.append(Thread(target=commands[1], args=(end_time,)))
    workers.append(Thread(target=commands[2]))

    for worker in workers:
        worker.setDaemon(True)
        worker.start()
    #Waits until the multithreading is complete
    for worker in workers:
        worker.join()

    return (system.sense,system.new_blue,system.temp_switch,datetime.datetime.now().time())

def save(data):
    try:
        day = str(datetime.date.today()).strip()
        with open('Data_Collection/office_single_detection_'+day+'.csv','a+') as f:
            f.write(str(data))
            f.write('\n')
            f.close()
    except:
        print "Unable to save data"
        raise

if __name__=="__main__":
    control_obj = functions.Functions()
    control_obj.bluetooth()
    timer = 1
    try:
        while True:
            end = int(time.time())+(timer*60)
            if int(control_obj.new_blue) == 0:
                print "Looping through bluetooth"
                control_obj.bluetooth() #Updates the bluetooth state
            else:
                current_data = run(timer) #Gathers the data
                while True:
                    if int(time.time())==(end - 20): #Collects the bluetooth right before next interval begins
                        control_obj.bluetooth()
                        time.sleep(2) #So that the bluetooth command doesn't fill space
                    if int(time.time())>=end:
                        print "Writing Data"
                        save(current_data)
                        break
    except KeyboardInterrupt:
        raise
