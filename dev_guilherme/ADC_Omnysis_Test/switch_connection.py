import urllib.request
import time

def switch_connection(IP_SWITCH,switch_port):
    
    addr=urllib.request.urlopen("http://"+str(IP_SWITCH)+"/:SP4TA:STATE:"+str(switch_port))
    time.sleep(2.0)
    
    return 