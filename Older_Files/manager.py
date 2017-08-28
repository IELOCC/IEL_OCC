#!/usr/bin/python2.7

import functions
import mac_man
import json
import time
import schedule
import datetime
import csv
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

class Manage(mac_man.Mac_Man,functions.Functions):
    valuer = 0;
    def __init__(self,data="",mac=""):
        full_date = datetime.datetime.now();day = full_date.day; month = full_date.month; year = full_date.year;
        self.data_storage = str(data)+'_'+str(month)+'_'+str(day)+'_'+str(year)+'.csv';
        self.data_storage = data
        self.mac_storage = mac
        try:
            super(Manage,self).__init__(self.mac_storage)
        except:
            print "initialize values"
            pass

    def email(self):
        # Create a text/plain message
        today = datetime.datetime.now().date()
        msg = MIMEMultipart()
        msg['Subject'] = 'Data for '+str(today)
        sender = 'iel.datacollection@gmail.com'
        reciever = 'trd4@me.com'
        msg['From'] = sender
        msg['To'] = reciever

        fileToSend = 'Data_Collection/'+self.data_storage
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
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        return None

    def save(self,data):
        print 'Saving...'
        try:
            writer = csv.writer(open('Data_Collection/'+self.data_storage,'a+'))
            writer.writerow(data)
        except:
            print "Unable to save data"

    def objective(self):
        self.valuer = 1
        print 'Running objective...'
        try:
            what_june_wants = [self.state_1['Switch'],self.state_1['Bluetooth'],self.state_1['Sensor'][1]]
        except:
            what_june_wants = []
        try:
            do = datetime.datetime.now()
            stuff = extract(day)
            stuff.insert(0,str(do))
            print 'Material to be saved:\t{}'.format(stuff)
            save(stuff)
            #day.update()
        except:
            print "Check extract"
        return stuff

if __name__=="__main__":
    me = Manage(data="JUNE_ECJ_RPITEST1",mac="store_mac.json")
    #day = initialize('store_mac.json')
    #storage_place = filename('JUNE_ECJ_RPITEST1')
    me.update()
    schedule.clear()
    while True:
        current = time.time()
        if int(current)%60 == 0:
            schedule.every(1).minute.do(me.objective())
            break
    print 'Program started at:\t{}'.format(current)
    while True:
        timer = datetime.datetime.now()
        if(timer.hour == 21 and timer.minute== 00):
            email(storage_place)
            sys.exit()

        schedule.run_pending()
        if valuer == 1:
            day.update()
            valuer = 0
