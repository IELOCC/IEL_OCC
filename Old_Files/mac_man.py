#!/usr/bin/python3.4

import functions
import sys
import re
import json

class Mac_Man(functions.Functions):
    def __init__(self,address): #each object is linked to this one address
        self.tracking = [] #initializes the empty tracking list
        self.switch = []
        self.address = address
        self.load()
#These are for the local lists - switch and tracking devices
    def check(self,mac): #This is a physical formatting verification
        #Any time this is called, we want it to test that the mac address is valid
        mac_format = re.compile('..:..:..:..:..:..') #Checks the formatting of the mac string
        return re.match(mac_format,mac.strip())
        #Can think about adding this later if it demands greater security
    def refresh(self): #removes duplicates from the lists. Should be automatically called regularly.
        self.tracking = list(set(self.tracking))
        self.switch = list(set(self.switch))
        return None
    def add(self,info):#Really the only function to be called
        #Adds the switchmate information
        if isinstance(info,tuple): #Adds the data regarding switchmate
            try:
                assert self.check(info[0])
                self.switch.append(info)
                self.refresh() #To avoid duplicate values
            except AssertionError:
                print("Could not add peripheral info")
            except IndexError:
                print("Add authorization code to update")
        elif isinstance(info,str): #Adds the tracking info
            try:
                assert self.check(info)
                self.tracking.append(info)
                self.refresh() #To avoid duplicates
            except AssertionError:
                print("Could not add tracking info")
        else:
            pass
        self.save() #Saves the added part
    def remove(self,info):
        if isinstance(info,tuple):
            if info in [i[0] for i in self.switch]: self.switch.remove(info)
            print("Removed switch.")
        elif isinstance(info,str):
            if info in [i.encode('utf-8') for i in self.tracking]: self.tracking.remove(info)
            print("Removed peripheral.")
        self.save()

    def prep(self,value=0): #This function preps the mac addresses for processing in the Functions method. Default is to take the first value
        try:
            assert self.tracking
            assert self.switch
            assert len(self.switch[value])==2
            prepped = (self.tracking[value],self.switch[value])
            super(Mac_Man, self).__init__(prepped)
        except:
            print("Problems with preparation")
#These are for the file storage system
    def reset(self): #Erase the contents of the file
        self.tracking = []
        self.switch = []
        with open(self.address,"w"):
            pass
    def load(self): #Grabs the data from the stored file
        try:
            with open(self.address,'a+') as json_data:
                data = json.load(json_data)
                adding_tracking = [self.add(item.encode('utf-8')) for item in data[0]]
                adding_switch = [self.add((item[0].encode('utf-8'),item[1].encode('utf-8'))) for item in data[1]]
        except (AttributeError, ValueError) as e:
            print("Data was not loaded.")
            self.data = [] #This is the default error state
    def save(self):
        #Can be used as a confirmation to verify that the data was indeed saved
        try:
            with open(self.address, 'w+') as f:
                json.dump((self.tracking,self.switch),f)
        except:
            print("Unable to save")
