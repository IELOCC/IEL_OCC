#!/usr/bin/python3.4
#import switch
#import ping_command
import sensor_collection
import sys
import time
import subprocess
from threading import Thread

class Functions(object):
    #State function: [0] -> Entering, [1] -> Exiting, [2] -> Lux, [3] -> Switch
    def __init__(self,mac):
        try:
            assert isinstance(mac[0],str)
            assert isinstance(mac[1],tuple)
            self.mac_tracking = mac[0]
            self.mac_switch = mac[1][0]
            self.switch_auth = mac[1][1]
        except (TypeError, AssertionError):
            print('Process the values with \'prep()\' first')
            raise TypeError
        self.new_sense = ();
        self.state_1 = {'Bluetooth':0,'Switch':0,'Sensor':0}; self.state = [0,0,0,0]; self.lux = 1;
#Current State is not running not has any use. Functionality will be to run all tasks and do full update to current state
    def update(self,delay=10):#This does a full scan for the environment, updating bluetooth logic switch pos and lux logic
        try:
            self.state_0 = self.state_1; self.new_sense = (); #Out with the old, in with the new
            #The values will be appended in random order due to the multithreading nature, dictionary formatting makes it possible to call them consistently based on naming convention
            commands = [self.bluetooth,self.switch_m,self.sensors]
            #Starts my threading list to maintain the integrity of the individual address
            workers = []
            #Defines the multithreading
            workers.append(Thread(target=commands[0], args=((delay),)))
            workers.append(Thread(target=commands[1], args=((delay),)))
            workers.append(Thread(target=commands[2]))
        except AssertionError:
            print('System was not initialized.')
            return None

        #Starts multithreading
        for worker in workers:
            worker.setDaemon(True)
            worker.start()

        #Waits until the multithreading is complete
        for worker in workers:
            worker.join()

        self.state_1 = dict(self.new_sense)
        #This section will pass our current state values into the logic gates we've built
        self.entering()
        self.exiting()
        self.lux_difference()
        self.switch_logic()
#Outputs an integer value
    def bluetooth(self,delay=10):#Treading: Pass Delay, Mac
        final = 0
        command = 'sudo timeout '+str(delay)+' l2ping -c 1 '+str(self.mac_tracking)
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if "0% loss" in out: final = 1
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Error with peripheral detection")
            pass
        self.new_sense += (['Bluetooth',final],) #updates the tuple state
        return final

    def switch_m(self,delay=10): #Sets the inital value
        end_time = time.time()+40 #Gives the function 40 seconds to get a value
        final = 0 #Confirms that the value was recorded. If return is 0, the status was not found
        sys.path.append('switchmate')
        command = 'sudo timeout '+str(delay)+' python switchmate/switchmate.py status '+self.mac_switch
        while final == 0 and int(time.time() < end_time):
            try:
                running = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = running.communicate()
                if 'on' in out: final = 1;
                if 'off' in out: final = -1;
            except (KeyboardInterrupt, SystemExit):
                print("EXITING")
            except:
                print("System fail. Thanks switchmate.")
        self.new_sense += (['Switch',final],)
        return final

    def sensors(self):
        final = sensor_collection.out()
        self.new_sense += (['Sensor',final],)
        return final

    ############################################################
    #Logic Functions for Q table
    def entering(self):
        if self.state_0['Bluetooth']==0 and self.state_1['Bluetooth']==1:
            self.state[0] = 1
        else:
            self.state[0] = 0
    def exiting(self):
        if self.state_0['Bluetooth']==1 and self.state_1['Bluetooth']==0:
            self.state[1] = 1
        else:
            self.state[1] = 0
    def lux_difference(self,light_threshold=50): #The default threshold is 50. Change in this function to tweak the precision.
        try:
            if self.state_1['Sensor'][1] > self.lux + light_threshold and self.state_1['Bluetooth']==1: #Basically says: If the light reading is significantly changed and prescence detected
                self.lux = self.state_1['Sensor'][1]
                self.state[2] = 1
            elif self.state_1['Sensor'][1] < self.lux - light_threshold and self.state_1['Bluetooth']==1:
                self.lux = self.state_1['Sensor'][1]
                self.state[2] = -1
            else:
                self.state[2] = 0
        except:
            self.state[2] = 0
    def switch_logic(self):
        try:
            self.state[3] = self.state_1['Bluetooth']
        except KeyError:
            self.state[3] = 0

    #Methods to interact with environment
    def switch_on(self):
        command = 'sudo python /switchmate/switchmate.py '+str(self.mac_switch)+' '+str(self.switch_auth)+' switch on'
        control = subprocess.Popen(command,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
        our,err = control.communicate()
        return None
    def switch_off(self):
        command = 'sudo python /switchmate/switchmate.py '+str(self.mac_switch)+' '+str(self.switch_auth)+' switch off'
        control = subprocess.Popen(command,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
        our,err = control.communicate()
        return None
