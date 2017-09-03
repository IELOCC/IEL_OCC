#!/usr/bin/python2.7
import subprocess

def status():
    try:
        with open ('store_mac.txt','r') as mac:
            mac = mac.read(); mac = mac.strip()
            command = "sudo l2ping -c 2 "+mac
            print command
            output = subprocess.check_output(command, shell=True,stderr=subprocess.STDOUT)
            print "No problem with the confirm.py function"
        return True
    except:
        return False

def ping():
    return None

def main():
    print "This is the status of the confirm.status():"
    print status()
    return None

if __name__=="__main__":
    main()
