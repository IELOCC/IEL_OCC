#!/usr/bin/env python

import subprocess
import os
import datetime
import operator
import schedule
import csv
import time
import smtplib
import mimetypes
import json
import sys
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

class Scanner:
    running_list = {}
    occupancy = []
    day = datetime.date.today();f_day = str(day.month)+'_'+str(day.day)+'_'+str(day.year)
    reboot = False

    def email(self,file_n):
        print 'Emailing...'
        # Create a text/plain message
        today = datetime.datetime.now().date()
        msg = MIMEMultipart()
        msg['Subject'] = 'Data for '+str(today)
        sender = 'iel.datacollection@gmail.com'
        reciever = 'iel.basdata@gmail.com'
        msg['From'] = sender
        msg['To'] = reciever

        fileToSend = file_n #We might consider passing this through the filename function to modify the name in the email
        username = "iel.datacollection@gmail.com"
        password = "ieloffice"

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username,password)
        server.sendmail(sender, reciever, msg.as_string())
        server.quit()
        return None
    def reset(self): #Really shouldn't be used, as the program will terminate in the morning
        self.running_list.clear()
    def sort(self):
        print 'Sorting...'
        return sorted(self.running_list, key=operator.itemgetter(1))
    def clean(self):
        print 'Cleaning...'
        off = subprocess.Popen('sudo hciconfig hci0 reset',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err = off.communicate()
        return None
    def run(self,timer=25):
        print 'Running...'
        command = "sudo timeout "+str(timer)+" hcidump [-a]"
        current = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err = current.communicate()
        return out
    def parse(self,raw_data):
        try:
	    p = raw_data
            mac = {}
	    #Splits the dump info into segments based on event
            j = p.split('HCI Event:')
            for i in range(len(j)): #For each bluetooth event
            	a = j[i].find('bdaddr') #Looks for the mac found
            	if a != -1 and "nd" not in j[i][a+7:a+24] and j[i][a+7:a+24] != "": #Filters events without mac address and exceptional cases
            	    mac_add = j[i][a+7:a+24]
		    b = j[i].find('RSSI')#Looks to see if RSSI in Event
            	    if b != -1:
                        start_point = b+7 #Arbitrary point that was found to begin the RSSI
                        end_point = start_point
                        bool_guy = True
                        while bool_guy: #This while loop keeps looking until the part isn't a digit. In this way we can manage variable length numbers
                            if j[i][end_point+1].isdigit():
                                end_point += 1
                            else:
                                bool_guy = False
                        mac[j[i][a+7:a+24]] = int(j[i][start_point:end_point+1]) #Value is recorded if found
            	    else:
			mac[j[i][a+7:a+24]] = None #If no RSSI, value is still recorded with NONE
            return mac
        except:
            return None
    def filt(self,macs):
        print 'Filtering...'
        #Adds data for histogram approach at volumetric measurement
        timeit = datetime.datetime.now()
        try: #If parse returns none, this will catch that
	    t = str(timeit),len(macs)
            self.occupancy = t #This adds the tuple containing time and occupancy volume to occupancy list
            self.RSSI = str(timeit),macs
            #Adds to the running counter of the day
            for k,v in macs.items():
                if k in self.running_list:
                    self.running_list[k]+=1
                else:
                    self.running_list[k]=1
	except TypeError:
	    self.occupancy = str(timeit),0
	    self.RSSI = str(timeit),macs        
	return None
    def update(self):
        print "Updating..."
        self.clean() #Cleans the bluetooth channel
        self.filt(self.parse(self.run())) #Runs our filtering techniques on the values
        print "New values"
	print self.RSSI
	self.reboot = False #For the timing module in the main function
    def write(self):
        print 'Saving...'
        #The following two lines append the current office profile volumetric data to the file
        writer_1 = csv.writer(open('Data_Collection/office_profile_'+self.f_day+'.csv','a+'))
        print "Writing Occupancy {}".format(self.occupancy)
	writer_1.writerow(self.occupancy)
        #Stores all of the data - timestamp and RSSI info
        with open('Data_Collection/office_profile_RSSI_'+self.f_day+'.csv','a+') as json_file:
            json.dump(self.RSSI,json_file)

        #The following writes a new file every time the system is called, maintaining the most current data format in case of file disruption. Consider adding a file reading mechanism at startup to recover the data in case of power outage
        with open('Data_Collection/office_cumulative_'+self.f_day+'.csv','w+') as f:
            writer_2 = csv.writer(f)
            for key, value in self.running_list.items():
                writer_2.writerow([key,value])
        with open('Data_Collection/office_total_'+self.f_day+'.txt','a+') as f:
            f.write(str(self.occupancy).strip('[]'))
            fin = ''
            for key, value in self.running_list.items():
                fin += str(key)+', '+str(value)+'\n'
            f.write(fin)
        self.reboot = True

if __name__=="__main__":
    my_scan = Scanner()
    my_scan.reset() #Cleans the bluetooth ports
    my_scan.update()
    schedule.every(1).minute.do(my_scan.write) #Builds a system scheduler to run every minute
    while True:
        timer = datetime.datetime.now()
        if timer.hour == 23 and timer.minute == 59: #Email everything at midnight
            my_scan.email('Data_Collection/office_profile_'+my_scan.f_day+'.csv')
            my_scan.email('Data_Collection/office_cumulative_'+my_scan.f_day+'.csv')
            sys.exit()
        schedule.run_pending()
        #Regularly refreshes the data
        if my_scan.reboot:
            my_scan.update()
