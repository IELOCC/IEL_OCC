import os
import sys
import schedule
import csv
import datetime
import time
import subprocess

update = True
Macs = []
#Does this work
def ping(ping_macs,delay=10):#Treading: Pass Delay, Mac
    print('Ping...')
    output = []
    for i in ping_macs:#only accepts lists
        clean()
        final = 0#sets our default off state
        command = 'sudo l2ping -c 1 '+str(i)#Here's the command of interest for the night
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = process.communicate()
        if "0% loss" in str(out): final = 1
        output.append(final)

    return output

def lescan(tracking, timer=10):
    print('LEscan...')
    #tracking = ['E2:7C:2D:4C:E2:B4','F6:97:2C:20:BE:E4']
    clean()
    devices = subprocess.Popen('sudo timeout '+str(timer)+' stdbuf -oL hcitool lescan', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = devices.communicate()

    #This whole segment is to help me understand output process
    if out:
        print("standard output of subprocess:")
        print(out)
    if err:
        print("standard error of subprocess:")
        print(err)
    print("returncode of subprocess:")
    print(devices.returncode)

    output = []
    for i in tracking:
        if i in str(out):
            output.append(1)
        else:
            output.append(0)
    return output

def email(self,file_n,name):
    print('Emailing...')
    try:
        print('Emailing...')# Create a text/plain message
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

def clean():
    print('Cleaning...')
    off = subprocess.Popen('sudo hciconfig hci0 reset',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err = off.communicate()

def multi(scan_macs,ping_macs):
    print('Initiating multi...')
    clean() #This cleans the bluetooth channel each time we scan
    data = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]    #Sets the time in the first column
    scan_out = lescan(scan_macs)        #Brings us information about the scanned devices
    ping_out = ping(ping_macs)          #Brings information about the pingged devices
    update = False
    return data+scan_out+ping_out

def save(dest,append_write,data):
    print('Saving...')
    with open(dest,append_write) as f:  #Writes data. Yaddah yaddah.
        writer = csv.writer(f)
        writer.writerow(data)

def updater():
    update = True

if __name__=="__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__)) #This is our current working path
    dest_dir = os.path.join(script_dir,'Multiping_Data') #Builds a path to the file we'd like to work with
    file_name = os.path.join(dest_dir,str(datetime.datetime.now().date())+'.csv') #Builds our file name

    try:
        os.makedirs(dest_dir) #Makes a directory for saving the data
        #save(file_name,append_write,header); #Only works if it's a new file
    except OSError:
        pass #If it can't make it then it must already exist

    #June's fitbit
    scan_macs = ['E5:7C:2D:4C:E2:B4']
    #Thomas iPhone, June's iPhone, Jose's phone, Zoltan's android
    ping_macs = ['4C:57:CA:78:44:C8','1C:5C:F2:79:35:56','D8:C4:6A:C4:35:05']#,'10:30:47:34:83:A0']

    to_email = ['juneyoungpark@utexas.edu','HagenFritz@utexas.edu','trdougherty@utexas.edu'] #Sends the data to these emails

    header = ['Time']; #Builds the first column of our new file
    #This builds our header
    for i in scan_macs:
        header.append(i);
    for i in ping_macs:
        header.append(i)

    if os.path.exists(file_name):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w+' # make a new file if not
        save(file_name,append_write,header);
        append_write = 'a' # after header is made, change this status

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
            data = multi(scan_macs,ping_macs)
            print(data)
            save(file_name,append_write,data)
