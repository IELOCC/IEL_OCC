#!/usr/bin/python2.7
import switch_2
import ping_command
import sensor_collection

class Functions:
    state = [0,0,0,0]
    old_blue = 0
    new_blue = 0
    temp_switch = 0
    lux = 1
    def output(self):
        bluetooth = 'Bluetooth:\t'+str(self.new_blue)+'\n'
        #switch = 'Switch:\t'+str(self.state[1])+'\n'
        return [bluetooth]#,switch]
    def update(self,mac):#,value): inserted mac for multi code
        self.new_blue = int(ping_command.time_ping(10,mac))
        #self.temp_switch = int(switch_2.main(10)) #THIS IS DIFFERENT FOR
        #self.entering(self.new_blue)
        #self.switch_status()
        #self.exiting(self.new_blue)
        #self.old_blue = self.new_blue
        #self.lux_difference(value)

    def entering(self,blue1):
        if self.old_blue==False and self.new_blue==True:
            self.state[0] = 1
        else:
            self.state[0] = 0

    def switch_status(self):
        if self.temp_switch!=0:
            self.state[1] = self.temp_switch

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
