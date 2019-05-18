from scapy.all import *
import signal
import sys
import os
import time
from multiprocessing import Process
from subprocess import Popen

clientss = []
apss = []
aps = {}
aps1 = []
interface_wifi = 'wlan2mon'
pcap = 'hd.pcap'

# write


def write(pkt):
    wrpcap(pcap, pkt, append=True)


def getAP(pkt):

    if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
        try:
            bssid = pkt[Dot11].addr3
        except:
            bssid = pkt[Dot11FCS].addr3
        # https://github.com/secdev/scapy/issues/1590
        # The problem is quite simple.
        # Since the latest versions, Dot11 may also be Dot11FCS depending on if there is a FCS or not.
        #print bssid
        if bssid not in apss:
            apss.append(bssid)


def no(pkt):
    if pkt.haslayer(Dot11):
        write(pkt)


# channels between 1-13
def channel_hop():
    while True:
        try:
            for i in range(1, 14):
                os.system('iw dev '+interface_wifi+' set channel %d' % (i))
                time.sleep(1)
        except KeyboardInterrupt:
            break


def signal_handler(sig, frame):
    p.terminate()
    p.join()
    sys.exit(0)


# p1=Popen(['airmon-ng','stop','wlan2mon'])
# alternative after mitm but it does not work
# cause wlan*mon has lost the monitor mode
# repair it with iwconfig
os.system('ifconfig '+interface_wifi+' down')
time.sleep(1)
os.system('iwconfig '+interface_wifi+' mode monitor')
time.sleep(1)
os.system('ifconfig '+interface_wifi+' up')
time.sleep(1)

p = Process(target=channel_hop)
p.start()
sniff(iface=interface_wifi, count=1000, prn=getAP,
      store=False)  # 1000 packets for discovering
# APS.txt -> dea2.py
with open('APS.txt', 'w') as f:
    for i in apss:
        f.write(i+'\n')

time.sleep(1)
print("Ready to sniff -> pcap")
sniff(iface=interface_wifi, count=10000, prn=write,
      store=False)  # 10000 packets for save
signal.signal(signal.SIGINT, signal_handler)
#without signal.pause there is exception by thread
#signal.pause() 
#sniff(iface='wlan1mon', prn=insert_ap, store=False,lfilter=lambda p: (Dot11Beacon in p or Dot11ProbeResp in p))
