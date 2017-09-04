#!/usr/bin/python3.4

import subprocess
import os
import datetime
import operator
import schedule
import csv
import time
import smtplib
import mimetypes
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
    day = datetime.date.today();f_day = str(day.year)+"-"+str(day.month)+"-"+str(day.day)
    reboot = False

    def name(self):
        return open('/home/pi/name','r').read().rstrip()
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
    def run(self):
        print 'Running...'
        timer = 15
        command = "sudo timeout "+str(timer)+" stdbuf -oL hcitool lescan"
        current = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err = current.communicate()
        return out.split('\n')
    def filt(self,macs):
        print 'Filtering...'
        temp = {}
        for i in macs[1:len(macs)]:
            if i != '':
                temp[i[0:17]] = 1

        #Adds data for histogram approach at volumetric measurement
        timeit = datetime.datetime.now()
        t = str(timeit),len(temp)
        self.occupancy = t #This adds the tuple containing time and occupancy volume to occupancy list
        #Adds to the running counter of the day
        for k,v in temp.items():
            if k in self.running_list:
                self.running_list[k]+=1
            else:
                self.running_list[k]=1
        return None
    def update(self):
        print "Updating..."
        self.clean()
        self.filt(self.run())
        self.reboot = False
    def write(self,BTD,MAC,TOT):
        print 'Saving...'
        #The following two lines append the current office profile volumetric data to the file
        with open(BTD,'a+') as f:
            writer_1 = csv.writer(f)
            writer_1.writerow(self.occupancy)
        #The following writes a new file every time the system is called, maintaining the most current data format in case of file disruption. Consider adding a file reading mechanism at startup to recover the data in case of power outage
        with open(MAC,'w+') as f:
            writer_2 = csv.writer(f)
            for key, value in self.running_list.items():
                writer_2.writerow([key,value])
        with open(TOT,'a+') as f:
            f.write(str(self.occupancy).strip('[]'))
            fin = ''
            for key, value in self.running_list.items():
                fin += str(key)+', '+str(value)+'\n'
            f.write(fin)
        self.reboot = True

if __name__=="__main__":
    #/home/pi/IEL_OCC/Data_Collection/
    script_dir = os.path.dirname(__file__)
    my_scan = Scanner()
    BTD = os.path.join(script_dir,'Data_Collection/BTD_'+my_scan.name()+'_'+my_scan.f_day+'.csv')
    MAC = os.path.join(script_dir,'Data_Collection/MAC_'+my_scan.name()+'_'+my_scan.f_day+'.csv')
    TOT = os.path.join(script_dir,'Data_Collection/TOT_'+my_scan.name()+'_'+my_scan.f_day+'.txt')
    my_scan.reset() #Cleans the bluetooth ports
    schedule.every(1).minute.do(my_scan.write,BTD,MAC,TOT) #Builds a system scheduler to run every minute
    while True:
        timer = datetime.datetime.now()
        if timer.hour == 23 and timer.minute == 59: #Email everything at midnight
            my_scan.email(MAC)
            my_scan.email(BTD)
            sys.exit()
        if timer.minute == 05:
            my_scan.email(BTD)
            time.sleep(60)
        if my_scan.reboot:
            my_scan.update()
        schedule.run_pending()
