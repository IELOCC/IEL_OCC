#!/usr/bin/python2.7

class Status:
    keys = {'confirmation':0,'mac_object':0,'mac_switch':0,'auth_switch':0,'bluetooth':0,'switch':0,'lux':1}
    def __init__(self):
        with open('confirmation','r') as f:
            temp = f.read()
        self.keys['confirmation'] = int(temp.strip())
    def get(self,param):
        try:
            return self.keys[param]
        except:
            print "Unable to set value, check key name"
    def set(self,param,value):
        try:
            self.keys[param] = value
            #Also setting the global variable by changing the storage script
            if param=='confirmation':
                with open(param,'w') as f:
                    f.seek(0)
                    f.write(str(value))
                    f.truncate()
                    f.close()
            return True
        except:
            print "Check your input parameter"
            return False
    def query(self):
        for key, value in self.keys.iteritems():
            print key, value

