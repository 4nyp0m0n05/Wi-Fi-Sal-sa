import requests
import sys
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#this lines above and below for ssl problems 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
try:
    page = requests.get(sys.argv[1])
except:
    try:
        page = requests.get(sys.argv[1], verify=False)
    except:
        page = requests.get(sys.argv[1], verify=False)
url1 = str(page.url).split('/')[0]+"//"+str(page.url).split('/')[2]+"/"
print(url1)
check2 = str(page.content)
#sau.web http 200 http://1.1.1.1
if "URL" in check2:
    http = check2.split(
        '//')[0].split("=")[len(check2.split('//')[0].split("="))-1]
    url1 = check2.split('//')[1].split("/")[0]
print(url1)
# changed url (redirected)
if sys.argv[1] != page.url:
    os.system('python3 gethtml.py '+url1+' 1')  # + http+'//'+url1+' 1')
else:
    os.system('python copyy.py 0')
    # copy default fake pages
