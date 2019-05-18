import os
import sys
import time
# essid="asdasd"
# essid=sys.argv[1]
interface_wifi = 'wlan2mon'
interface_connect = 'wlan0'
open_ap = []
essid = ''
# change OPN with WEP/WPA/WPA2 or whatever you want to select a fake AP (first match) in aps.txt
"""
with open("aps.txt") as f:
    open_ap=f.readlines()
for i in open_ap:
    if "OPN" in i and "null" not in i:
        essid=i.split(" ")[1]
        break
"""
try:
    essid = sys.argv[1]
except:
    essid = ''
print essid


def connect():
    #after mitm it has an ip like 10.0.0.1 interface_wifi    
    os.system("ifconfig "+interface_wifi+" inet 0.0.0.0")
    #we need stop network manager if we want connect
    os.system("service network-manager stop")
    os.system("ifconfig "+interface_connect+" up")
    os.system("iwconfig "+interface_connect+" essid "+essid)
    os.system("dhclient "+interface_connect)
    # if we connected probably it will redirect the login page with google.com
    os.system("python3 check.py http://google.com")


def disconnect():
    os.system("ifconfig "+interface_connect+" down")
    os.system("dhclient -r "+interface_connect)
    os.system("service network-manager start")
    #maybe cause an error like not connected for Wi-Fi after we want to run another command in last.py 
    #for not to be a trouble
    with open("control", 'w') as f:
        f.write("1")


connect()
time.sleep(5)
disconnect()
