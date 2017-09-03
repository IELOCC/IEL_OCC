#!/usr/bin/python2.7

def modify(filename,text):
    with open(filename,'r+') as f:
        f.seek(0)
        f.write(text)
        f.truncate()
        f.close()

modify('store_mac.txt','')
modify('confirmed','0')
modify('ping_output','')
