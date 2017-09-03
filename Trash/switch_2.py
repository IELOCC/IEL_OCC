import sys
import os
import subprocess
import time
import signal

final = 0

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)

#This grabs the mac address from the light
def build_command(delay):
    sys.path.append('switchmate')
    switch_mac = open('switchmate/switch_mac','r+')
    switch_mac = switch_mac.read(); switch_mac = switch_mac.strip()
    pass_location = 'sudo timeout '+str(delay)+' ./switchmate/switchmate.py'
    pass_function = ' status '+switch_mac
    cmd = pass_location+pass_function
    return cmd

def logic(out,err):
    global final
    global attempt_number
    global build
    if 'on' in out:
        final = 1
    elif 'off' in out:
        final = -1
    return final

def main(delay):
    global final
    global attempt_number

    #Defines command
    cmd = build_command(delay)
    try:
        #Define the action being taken
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # wait for the process to terminate
        out, err = process.communicate()
        final = logic(out,err)
    except (KeyboardInterrupt, SystemExit):
        print "EXITING"
    except:
        print "Couldn't build"
        pass
    return final

if  __name__ =="__main__":
    print main(10)


