from scapy.all import *
import signal
import sys
from subprocess import Popen, PIPE
import os
from multiprocessing import Process

interface_wifi='wlan2mon'
pcap='a.pcap'
details = []
clientss = []
aps = {}
aps1 = []
#wps https://github.com/devttys0/wps/blob/master/wpstools/wpspy.py
elTags = {
    'SSID': 0,
    'Vendor': 221
}
# Dictionary of relevent WPS tags and values
wpsTags = {
    'APLocked': {'id': 0x1057,    'desc': None},
    'WPSUUID-E': {'id': 0x1047,    'desc': None},
    'WPSRFBands': {'id': 0x103C,    'desc': None},
    'WPSRegistrar': {'id': 0x1041,    'desc': None},
    'WPSState': {'id': 0x1044,    'desc': {
        0x01: 'Not Configured',
        0x02: 'Configured'
    }
    },
    'WPSVersion': {'id': 0x104a,    'desc': {
        0x10: '1.0',
        0x11: '1.1'
    }
    },
    'WPSRegConfig': {'id': 0x1053,    'desc': {
        0x0001: 'USB',
        0x0002: 'Ethernet',
        0x0004: 'Label',
        0x0008: 'Display',
        0x0010: 'External NFC',
        0x0020: 'Internal NFC',
        0x0040: 'NFC Interface',
        0x0080: 'Push Button',
        0x0100: 'Keypad'
    },
        'action': 'or'
    },
    'WPSPasswordID': {'id': 0x1012,    'desc': {
        0x0000: 'Pin',
        0x0004: 'PushButton'
    }
    }

}



def strToInt(string):
    intval = 0
    shift = (len(string)-1) * 8

    for byte in string:
        try:
            intval += int(ord(byte)) << shift
            shift -= 8
        except Exception, e:
            print 'Caught exception converting string to int:', e
            return False
    return intval


def getWPSInfo(elt):
    data = None
    tagNum = elt.ID
    wpsInfo = {}
    minSize = offset = 4
    typeSize = versionSize = 2

    # ELTs must be this high to ride!
    if elt.len > minSize:
            # Loop through the entire ELT
        while offset < elt.len:
            key = ''
            val = ''

            try:
                # Get the ELT type code
                eltType = strToInt(elt.info[offset:offset+typeSize])
                offset += typeSize
                # Get the ELT data length
                eltLen = strToInt(elt.info[offset:offset+versionSize])
                offset += versionSize
                # Pull this ELT's data out
                data = elt.info[offset:offset+eltLen]
                data = strToInt(data)
            except:
                return False

                # Check if we got a WPS-related ELT type
            for (key, tinfo) in wpsTags.iteritems():
                if eltType == tinfo['id']:
                    if tinfo.has_key('action') and tinfo['action'] == 'or':
                        for method, name in tinfo['desc'].iteritems():
                            if (data | method) == data:
                                val += name + ' | '
                        val = val[:-3]
                    else:
                        try:
                            val = tinfo['desc'][data]
                        except Exception, e:
                            val = str(hex(data))
                    break

            if key and val:
                wpsInfo[key] = val
            offset += eltLen
    return wpsInfo



WPS_ID = "\x00\x50\xF2\x04"
wps_attributes = {
    0x104A: {'name': 'Version                          ', 'type': 'hex'},
    0x1044: {'name': 'WPS State                        ', 'type': 'hex'},
    0x1057: {'name': 'AP Setup Locked                  ', 'type': 'hex'},
    0x1041: {'name': 'Selected Registrar               ', 'type': 'hex'},
    0x1012: {'name': 'Device Password ID               ', 'type': 'hex'},
    0x1053: {'name': 'Selected Registrar Config Methods', 'type': 'hex'},
    0x103B: {'name': 'Response Type                    ', 'type': 'hex'},
    0x1047: {'name': 'UUID-E                           ', 'type': 'hex'},
    0x1021: {'name': 'Manufacturer                     ', 'type': 'str'},
    0x1023: {'name': 'Model Name                       ', 'type': 'str'},
    0x1024: {'name': 'Model Number                     ', 'type': 'str'},
    0x1042: {'name': 'Serial Number                    ', 'type': 'str'},
    0x1054: {'name': 'Primary Device Type              ', 'type': 'hex'},
    0x1011: {'name': 'Device Name                      ', 'type': 'str'},
    0x1008: {'name': 'Config Methods                   ', 'type': 'hex'},
    0x103C: {'name': 'RF Bands                         ', 'type': 'hex'},
    0x1045: {'name': 'SSID                             ', 'type': 'str'},
    0x102D: {'name': 'OS Version                       ', 'type': 'str'}
}


def doprobee(pkt):
    #bssid = packet[Dot11].addr3.upper()
    # while Dot11Elt in pkt:
    wpsinfo = False
    ssid = ""
    tmp = ""
    while Dot11Elt in pkt:
        pkt = pkt[Dot11Elt]

        if pkt.ID == elTags['SSID']:
            ssid = pkt.info

        elif pkt.ID == elTags['Vendor']:
            wpsinfo = getWPSInfo(pkt)
        if wpsinfo != False:
            if type(wpsinfo) == dict and len(wpsinfo) > 0:
                print "SSID %s WPS %s" % (ssid, wpsinfo)
                tmp = str(ssid)+" "+str(wpsinfo)
                if tmp not in details:
                    details.append(tmp)

        pkt = pkt.payload

#save
def write(pkt):
    wrpcap(pcap, pkt, append=True) 




"""
def PacketHandlerr(pkt):

    if pkt.haslayer(Dot11):
        # if pkt.type in [1, 2]:
         #  print "%s %s" %(pkt.addr1, pkt.addr2)
        write(pkt)
        if pkt.type == 0 and pkt.subtype == 8:
            if pkt.addr2 not in aps:
                aps.append(pkt.addr2)
                print "%s %s %s" % (pkt.addr1, pkt.addr2, pkt.info)
        if pkt.type in [1, 2]:
            if pkt.addr1 not in aps and pkt.addr1 not in clientss:
                clientss.append(pkt.addr1)

            if pkt.addr2 not in aps and pkt.addr2 not in clientss:
                clientss.append(pkt.addr2)
"""

def insert_ap(pkt):
    # Done in the lfilter param
    # if Dot11Beacon not in pkt and Dot11ProbeResp not in pkt:
    #     return
    #print 'WPS support %s'% (getWPSInfo(pkt))
    # https://stackoverflow.com/questions/21613091/how-to-use-scapy-to-determine-wireless-encryption-type
    write(pkt)
    if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
        doprobee(pkt)
        try:
            bssid = pkt[Dot11].addr3  # Dot11 ve Dot11FCS dif classes :/ 
        except:
            bssid = pkt[Dot11FCS].addr3
            #https://github.com/secdev/scapy/issues/1590
            #The problem is quite simple. 
            #Since the latest versions, Dot11 may also be Dot11FCS depending on if there is a FCS or not.
        if bssid in aps:
            return
        p = pkt[Dot11Elt]
        cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                          "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
        ssid, channel = None, None
        crypto = set()
        while isinstance(p, Dot11Elt):
            if p.ID == 0:
                ssid = p.info
            elif p.ID == 3:
                channel = ord(p.info)
            elif p.ID == 48:
                crypto.add("WPA2")
            elif p.ID == 221 and p.info.startswith('\x00P\xf2\x01\x01\x00'):
                crypto.add("WPA")
            p = p.payload
        if not crypto:
            if 'privacy' in cap:
                crypto.add("WEP")
            else:
                crypto.add("OPN")
        print "NEW AP: %r [%s], channed %d, %s " % (
            ssid, bssid, channel, ' / '.join(crypto))
        tmp = str(ssid)+" "+str(bssid)+" "+str(channel)+" "+' / '.join(crypto)
        if tmp not in details:
            details.append(tmp)
        aps[bssid] = (ssid, channel, crypto)
        if ssid == '\x00':
            ssid = 'null'
        aps1.append(bssid+" "+ssid+" "+' / '.join(crypto))
        #aps1.append(channel)
    if pkt.haslayer(Dot11):

        if pkt.type in [1, 2]:
            if pkt.addr1 not in aps and pkt.addr1 not in clientss:
                clientss.append(pkt.addr1)

            if pkt.addr2 not in aps and pkt.addr2 not in clientss:
                clientss.append(pkt.addr2)

#change channel between 1-13
def channel_hop():
    while True:
        try:
            for i in range(1, 14):
                os.system('iw dev '+interface_wifi+' set channel %d' % (i))
                time.sleep(1)
        except KeyboardInterrupt:
            break

#before kill program save credentials
#mode w not append
def signal_handler(sig, frame):
    p.terminate()
    p.join()
    print("dead scapydeter.py")
    with open('clients.txt', 'w') as f:
        for i in clientss:
            f.write(str(i)+'\n')
    with open('aps.txt', 'w') as f:
        for i in aps1:
            f.write(str(i)+'\n')
    with open('details.txt', 'w') as f:
        for i in details:
            f.write(str(i)+'\n')
    sys.exit(0)



# sniff(iface='wlan1mon',prn=PacketHandlerr)
#p1=Popen(['airmon-ng','stop','wlan2mon']) #alternative after mitm but it does not work
                                           #cause wlan*mon has lost the monitor mode 
                                           #repair it with iwconfig
# p11.poll()
os.system('ifconfig '+interface_wifi+' down')
time.sleep(1)
os.system('iwconfig '+interface_wifi+' mode monitor')
time.sleep(1)
os.system('ifconfig '+interface_wifi+' up')
time.sleep(2)

#time.sleep(10)
p = Process(target=channel_hop)
p.start()

sniff(iface=interface_wifi, prn=insert_ap, store=False)
#sniff(iface=interface_wifi, prn=insert_ap, store=False,count=10000) #get 10k packets and stop
#https://stackoverflow.com/questions/28292224/scapy-packet-sniffer-triggering-an-action-up-on-each-sniffed-packet
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.pause()
#sniff(iface='wlan1mon', prn=insert_ap, store=False,lfilter=lambda p: (Dot11Beacon in p or Dot11ProbeResp in p))
