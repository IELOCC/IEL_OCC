#!/usr/bin/python3.4

import sys
import os
import re

def write():
    confirmed = False
    mac_format = re.compile('..:..:..:..:..:..')
    while(not confirmed):
        mac = raw_input('Please enter valid mac address: \t')
        print "Processing..."
        confirmed = re.match(mac_format,mac.strip())
    return mac
def store(address):
    with open('store_mac.txt','w') as f:
        f.seek(0)
        f.write(address)
        f.truncate()
        f.close()
    return None

def main():
    store(write())

if __name__=="__main__":
    main()
confirmed = False
mac_format = re.compile('..:..:..:..:..:..')

while(not confirmed):
    mac = input('Please enter valid mac address: \t')
    confirmed = re.match(mac_format,mac)

with open('store_mac.txt','r+') as f:
    f.seek(0)
    f.write(mac)
    f.truncate()
    f.close()


