#WiFi Sal-sa (Wi-Fi Saldırı-Savunma)
This project contains 802.11 network attacks and prevention/attention software.
Scripts are running via bluetooth. BlServ is attacking software and defender is prevention/attention software.
#Attack
##Attack Script Parameters (last.py)
    -Bagdriving (passive informations) 
    -Handshake (+deauth ) 
    -MiTM (internet connection) 
    -MiTM (without internet connection)
    -Copy Login Page
    -Deauthentication

##BlServ Parameters
    -Bagdriving -> 1
    -Handshake -> 2
    -Handshake with deauth -> first send 2 and after send 3
    -MiTM (internet connection) -> 6 ssid_name
    -MiTM (without internet connection) -> 7 eth0 ssid_name
    -Kill Running Process -> 5
    -Copy Login Page -> 9 ssid_name
    -Copy Default Fake Page ->11
    -Read outputs.txt (outputs last.py)-> 10
    -Read MiTM data -> 13
    -Deauthentication ->8
    -Restart RPi -> 12
    -Kill bluetooth connection ->4

#Prevention/Attention
#SSIDChecker supported by github.com/xnart
If there are different type same ssid with different credentials (if service is running) notify the situation for APs.

#TestInet supported by github.com/mek-12
Checks network connection if connection exist it checks SSLs of some pages if they are real or fake https sites with free SSLs.

#Defender
It contains DeauthDbm which shows us the distance between us with deauth attacker (it runs in RPi and we can see details in defender app. We need walk around for find the place of victim with RPi)(Wardriving) and HandshakeBlur which listen deauth packets and if finds them, it starts connecting with fake password which makes wrong EAPOLs so attacker gains fake password(if pcap not sliced)

nginx.conf supported by github.com/xnart. It is for redirection a website with punycode which running ssl.

