#!/usr/bin/python2.7

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
import os

def email(file_n):
    # Create a text/plain message
    today = datetime.datetime.now().date()
    msg = MIMEMultipart()
    msg['Subject'] = 'Data for '+str(today)
    sender = 'iel.datacollection@gmail.com'
    reciever = 'trdougherty@utexas.edu'
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

def filename(name):
    prefix = os.getcwd()
    date = datetime.datetime.now()
    stuff = [name,date.month,date.day,date.year]
    return str(prefix)+'/Data_Collection/'+'_'.join([str(i) for i in stuff])+'.csv'

def initialize(location):
    print 'Initializing...'
    #Create an object representing the day
    location = os.getcwd()+'/'+location #Defines the absolute path for the instance
    day = mac_man.Mac_Man(location)
    #This gathers the object in a coherent state
    day.prep()
    #Creates extractable data for us
    day.update()
    return day

def save(data,location):
    print 'Saving...'
    try:
        writer = csv.writer(open(location,'a+'))
        writer.writerow(data)
    except:
        print "Unable to save data"

def objective(day,location):
    global valuer; valuer = 1;
    print 'Running objective...'
    try:
        do = datetime.datetime.now()
        stuff = extract(day)
        stuff.insert(0,str(do))
        print 'Material to be saved:\t{}'.format(stuff)
        save(stuff,location) #Where this location doesn't need to be modified, as it's being modified in save()
        #day.update()
    except:
        print "Check extract"
    return stuff

def extract(obj):
    print 'Extracting...'
    try:
        sensor_data = [obj.state_1['Switch'],obj.state_1['Bluetooth'],obj.state_1['Sensor'][1]]
    except:
        sensor_data = []
    return sensor_data

if __name__=="__main__":
    valuer = 0;
    mac_storage = 'zoltan.json'
    file_name = 'JUNE_ECJ_RPITEST1'
    day = initialize(mac_storage)
    storage_place = filename(file_name)

    print 'The filename will be {}'.format(storage_place)
    schedule.clear()

    while True:
        current = time.time()
        if int(current)%60 == 0:
            schedule.every(1).minute.do(objective,day,storage_place)
            break
    print 'Program started at:\t{}'.format(current)

    while True:
        timer = datetime.datetime.now()
        if(timer.hour == 23 and timer.minute== 59):
            email(storage_place)
            sys.exit()

        schedule.run_pending()
        if valuer == 1:
            day.update()
            valuer = 0
