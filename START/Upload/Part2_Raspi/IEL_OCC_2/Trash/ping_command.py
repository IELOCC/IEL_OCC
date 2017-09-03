#!/usr/bin/python2.7
import subprocess
import signal
import time
import os

#THIS IS ALL TIMING CODE
#class TimeoutException(Exception):
#    pass
#def timeout_handler(signum, frame):
#    raise TimeoutException

#signal.signal(signal.SIGALRM, timeout_handler)

#SINGLE PING, RESURSION IS HANDLED IN PYTHON
with open('store_mac.txt','r') as f:
    mac = f.read()
    f.close()

#command = 'sudo l2ping -c 1 '+str(mac.strip())

def time_ping(delay,mac_addr):#modified to accomodate multiple addresses
    #signal.alarm(delay)
    return_val = 0
    command = 'sudo timeout '+str(delay)+' l2ping -c 1 '+str(mac_addr.strip())
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if "0% loss" in out:
            return_val=1
        #time.sleep(delay)
#    except TimeoutException:
#        pass
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print "Error with subprocess"
        pass

    return return_val

def main():
    time_ping(10)

if __name__=="__main__":
    main()
