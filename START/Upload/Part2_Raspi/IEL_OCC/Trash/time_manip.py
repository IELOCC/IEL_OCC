import os
import sys
import datetime

def format():
    with open('saved_time') as st:
        data = st.read()

    with open('presence') as pr:
        there = pr.read()
        there = there[0]

    M = data.find('m')
    S = data.find('s')
    result = str(there)+','+data[M+1:S]+','+str(datetime.datetime.now())
    return result

if __name__ == "__main__":
    obj = format()
    print(obj)
