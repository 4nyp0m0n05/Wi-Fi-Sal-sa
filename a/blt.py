from bluetooth import *
import os
import sys
import signal
import time
from multiprocessing import Process

import subprocess
from scapy.all import *



import math
import threading
last_val = []
ap_macs = {}
ssid_bssid = {}
ap_name="denemedeneme"
password="2985yhwfd9g238rg9"
clientss = []
interface_wifi='wlan2mon'
interface_conn='wlan0'
packet_count=5

print scapy.VERSION

count = 1
n = 2
l = 0.125
d0 = 1
PLd0 = 10*n*math.log10((4*math.pi*d0)/l)
aps = {}
aps1 = []
data = ''

def handshaker(arg1, arg2=""):
    global count
    ssid = arg1
    fake_pass = arg2
    os.system('sudo service NetworkManager stop')
    os.system("sudo wpa_passphrase "+ssid+" "+fake_pass+" >abc.txt")

    while count:
        print(str(count)+"-----------------------------------")
        os.system('ifconfig '+interface_conn+' up')
        p1 = subprocess.Popen(
            ["sudo", "wpa_supplicant", "-Dnl80211", "-i"+interface_conn, "-cabc.txt"])
        time.sleep(5)

        p2 = subprocess.Popen(['ps', '-a'], stdout=subprocess.PIPE)
        out, err = p2.communicate()
        for line in out.splitlines():
            if "wpa_supplicant" in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
        print "_________________________________________________________"
    print("You are here")
    p4 = subprocess.Popen(['ps', '-a'], stdout=subprocess.PIPE)
    out, err = p4.communicate()
    for line in out.splitlines():
        if "wpa_supplicant" in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
        print "_________________________________________________________"

    os.system('sudo service NetworkManager start')
    print('There')

    os.system('sudo service NetworkManager start')



t1 = threading.Thread(name="t1", target=handshaker,
                      args=(ap_name, password)


def PacketHandlerr1(pkt):
    global t1
    
    if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
        
        p = pkt[Dot11Elt]
        try:
            bssid = pkt[Dot11].addr3
        except:
            bssid = pkt[Dot11FCS].addr3
        if bssid in aps:
            return
       
        while isinstance(p, Dot11Elt):
            if p.ID == 0:
                ssid = p.info
            p = p.payload
            
        if str(bssid) not in ssid_bssid.keys():
            
            ssid_bssid[str(bssid)] = str(ssid)
            
    
    
    if pkt.haslayer(Dot11) or pkt.haslayer(Dot11FCS):
        #12 dea 10 dissas
        if pkt.type == 0 and (pkt.subtype == 12):
            
            if str(pkt.addr2) not in ap_macs.keys():
                ap_macs[str(pkt.addr2)] = 1
                
            else:
                ap_macs[str(pkt.addr2)] = ap_macs.get(str(pkt.addr2))+1
                
            if not t1.isAlive() and ap_macs.get(str(pkt.addr2)) > packet_count:
                
                count = 1

                
                print pkt.addr2
                ap_macs[str(pkt.addr2)] = 0
                print('3')
                
                t1 = threading.Thread(name="t1", target=handshaker, args=(
                    ap_name, password))
                t1.start()
                print(t1.isAlive())
                print count
                


def run2():
    sniff(iface=interface_wifi, prn=PacketHandlerr1, store=True)




def calcD(dBm):
    return math.pow(10.0, (math.fabs(-1*dBm-PLd0))/(10*n))


def PacketHandlerr(pkt):
    
    if pkt.haslayer(Dot11) or pkt.haslayer(Dot11FCS):
        
        if pkt.type == 0 and (pkt.subtype == 12 or pkt.subtype == 10):  # 12 dea 10 dissas
            if pkt.addr2:
                
                print "%s %s " % (pkt.addr1, pkt.addr2)
                print calcD(pkt.dBm_AntSignal)
                print pkt.dBm_AntSignal
                if connection == True:
                    try:
                        client_sock.send("%s %s %s %s" % (
                            pkt.addr1, pkt.addr2, pkt.dBm_AntSignal, calcD(pkt.dBm_AntSignal)))
                        time.sleep(2)
                    except:
                        print("ERROR")


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






def run():
    
    sniff(iface=interface_wifi, prn=PacketHandlerr, store=True)





def control_write(data):
    with open("control1", 'w') as f:
        f.write(str(data))


def control_read():
    with open("control1", 'r') as f:
        return int(f.read())


control_write(1)

connection = False
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = ""#uuid

advertise_service(server_sock, "Server", service_id=uuid, service_classes=[
                  uuid, SERIAL_PORT_CLASS], profiles=[SERIAL_PORT_PROFILE])


while True:
    control = control_read()
    while connection == False:
        print("Waiting connection")
        client_sock, client_info = server_sock.accept()
        connection = True
        print("Conn:", client_info)
    try:
        data = client_sock.recv(1024)
        client_sock.send("%s" % data)

    except:
        print "Error recv data"
        client_sock, client_info = server_sock.accept()
        connection = True
    if control == 0 and data != "3":
        try:
            client_sock.send("\nThere is running process")
        except:
            print "Error client lost"
            client_sock, client_info = server_sock.accept()
            connection = True

    if data == "3":
        try:
            tmp = last_val[-1]
        except:
            tmp = 0
        client_sock.send("%s" % data)

        if tmp == "1":
            try:
                p.terminate()
                p.join()
                p1.terminate()
                p1.join()
            except:
                p.terminate()
                p.join()
                p1.terminate()
                p1.join()

        elif tmp == "2":
            
            count = 0
            print("You are here")
            p4 = subprocess.Popen(['ps', '-a'], stdout=subprocess.PIPE)
            out, err = p4.communicate()
            for line in out.splitlines():
                if "wpa_supplicant" in line:
                    pid = int(line.split(None, 1)[0])
                    os.kill(pid, signal.SIGKILL)
            print "_________________________________________________________"

            os.system('sudo service NetworkManager start')
            print('There')
            
            try:
                p2.terminate()
                p2.join()
                p3.terminate()
                p3.join()

            except:
                print("You are here")
                p4 = subprocess.Popen(['ps', '-a'], stdout=subprocess.PIPE)
                out, err = p4.communicate()
                for line in out.splitlines():
                    if "wpa_supplicant" in line:
                        pid = int(line.split(None, 1)[0])
                        os.kill(pid, signal.SIGKILL)
                print "_________________________________________________________"

                os.system('sudo service NetworkManager start')
                print('There')

                p2.terminate()
                p2.join()
                p3.terminate()
                p3.join()

        control_write(1)

    if control > 0:
        try:
            if data == "1":
                print "Hello"
                last_val.append("1")
                control_write(0)
                p = Process(target=channel_hop)
                p.start()
                p1 = Process(target=run)
                p1.start()
            elif data == "2":
                print "Hi"
                
                count = 1
                last_val.append("2")
                control_write(0)
                p2 = Process(target=channel_hop)
                p2.start()
                p3 = Process(target=run2)
                p3.start()
                t1 = threading.Thread(name="t1", target=handshaker, args=(
                    ap_name, password))

        except IOError:
            print "Connection IOError"
            client_sock.close()
            connection = False
            pass
        except BluetoothError:
            print("Ble Error")
        except KeyboardInterrupt:
            print("Keyboard Int")
            client_sock.close()
            server_sock.close()
            break
