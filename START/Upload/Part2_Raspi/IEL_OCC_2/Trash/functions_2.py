#!/usr/bin/python255555.7
import switch_2
import ping_command
import sensor_collection
import time
import subprocess

class Functions:
    state = [0,0,0,0]
    old_blue = 0
    new_blue = 0
    temp_switch = 0
    lux = 1;sense = []
    mac ='4C:57:CA:78:44:C8'
    mac_switch = 'de:06:c6:fa:47:95'
    mac_auth = '60A80E8D'
    timer = 10

    def update(self,mac):#,value): inserted mac for multi code
        self.new_blue = int(ping_command.time_ping(10,mac))
        #self.temp_switch = int(switch_2.main(10)) #THIS IS DIFFERENT FOR
        #self.entering(self.new_blue)
        #self.switch_status()
        #self.exiting(self.new_blue)
        #self.old_blue = self.new_blue
        #self.lux_difference(value)
        #put something here about updating state of light switch to 0 again from the on/off position
        #self.temp_switch = 0

    #These functions are for multithreading###################
    def bluetooth(self):
        bluetooth_value = int(ping_command.time_ping(self.timer,self.mac))
        self.new_blue = bluetooth_value
        print "Completed bluetooth scan"

    def switch_sample(self,end):
        #Resets the temp switch so there's no carry over
        self.temp_switch = 0
        #Gives the function a full extra minute to cycle through the final argument
        while self.temp_switch == 0 and int(time.time())<(end-60):
            self.switch_status()

        if self.temp_switch != 0:
            self.state[1] = self.temp_switch

    def switch_status(self):
        switch = int(switch_2.main(self.timer))
        self.temp_switch = switch
        print "Completed switch scan"

    def sensors(self):
        sensors = sensor_collection.out()
        self.sense = sensors
        print "Completed sensor scan"
    ############################################################

    def entering(self,blue1):
        if self.old_blue==False and self.new_blue==True:
            self.state[0] = 1
        else:
            self.state[0] = 0

    def clean(self):
        off = subprocess.Popen('sudo hciconfig hci0 reset',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err = off.communicate()
        return None

    def switch_action(self,value):
        self.clean()
        command = 'sudo ./switchmate/switchmate.py '+self.mac_switch+' '+self.mac_auth+' switch '
        if int(value) == 1:
            command+='on'
        else:
            command+='off'
        current = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err = current.communicate()
        print "out is: "+out
        print "err is: "+err
        return None

    def lux(self):
        return sensor_collection.lux()

    def lux_difference(self,value1):
        try:
            if value1>self.lux+50 and self.new_blue==1:
                self.lux = value1
                self.state[2] = 1
            elif value1<self.lux-50 and self.new_blue==1:
                self.lux = value1
                self.state[2] = -1
            else:
                self.state[2] = 0
        except:
            self.state[2] = 0

    def exiting(self,value1):
        if self.old_blue==1 and self.new_blue==0:
            self.state[3] = 1
        else:
            self.state[3] = 0
