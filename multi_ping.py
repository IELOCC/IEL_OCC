import os
import sys
import schedule
import csv
import datetime
import time

update = True
Macs = []

def bluetooth(address,delay=10):#Treading: Pass Delay, Mac
    final = 0
    command = 'sudo timeout '+str(delay)+' l2ping -c 1 '+str(address)
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if "0% loss" in out: final = 1
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Error with peripheral detection")
        pass
    #self.new_sense += (['Bluetooth',final],) #updates the tuple state
    return final

def email(self,file_n,name):
    try:
        print 'Emailing...'# Create a text/plain message
        today = datetime.datetime.now().date()
        msg = MIMEMultipart()
        msg['Subject'] = 'Data for '+str(today)
        sender = 'iel.datacollection@gmail.com'
        reciever = name#'iel.basdata@gmail.com'
        msg['From'] = sender
        msg['To'] = name#reciever

        fileToSend = file_n #We might consider passing this through the filename function to modify the name in the email
        username = "iel.datacollection@gmail.com"
        password = "ieloffice"

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)
        if maintype == "text":
            fp = open(fileToSend)    # Note: we should handle calculating the charset
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
        attachment.add_header("Content-Disposition","attachment",filename=fileToSend)
        msg.attach(attachment)
        server=smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username,password)
        server.sendmail(sender,reciever,msg.as_string())
        server.quit()
        return None
    except:
        pass

def clean(self):
    print 'Cleaning...'
    off = subprocess.Popen('sudo hciconfig hci0 reset',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err = off.communicate()

def multi(devices):
    data = []
    data.append(datetime.datetime.now())
    for i in devices:
        data.append(bluetooth(i)) #This stores the values as a tuple in a consistent manner (blue_mac, occ)
    update = False
    return data

def save(dest, data):
    with open(dest,'a+') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def updater():
    update = True

if __name__=="__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir,'Multiping_Data') #Builds a path to the file we'd like to work with
    try:
        os.makedirs(dest_dir) #Makes a directory for saving the data
    except OSError:
        pass
    #June's fitbit, Thomas iPhone, Zoltan's android
    Macs = ['E5:7C:2D:4C:E2:B4','4C:57:CA:78:44:C8']#,'10:30:47:34:83:A0']
    file_name = os.path.join(dest_dir,datetime.datetime.today(),'.csv') #This puts a datestamp on the file name
    to_email = ['juneyoungpark@utexas.edu','HagenFritz@utexas.edu','trdougherty@utexas.edu'] #Sends the data to these emails

    header = ['Time'];for i in Macs: header.append(i); save(dest_dir,header); #This puts headers on the columns we're working with
    clean(); #This cleans the bluetooth channel
    schedule.every(1).minute.do(updater) #Makes a function that runs every minute
    while True:
        timer = datetime.datetime.now()
        if timer.hour == 23 and timer.minute == 59: #Email everything at midnight
            for i in to_email:
                email(file_name,i)
                time.sleep(3)
            sys.exit()
        if update:
            thing = multi(Macs)
            print thing
            save(dest_dir,thing);

