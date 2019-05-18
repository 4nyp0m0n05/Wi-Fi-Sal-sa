import sys
import os
val = int(sys.argv[1])
# without this can't be generated file
os.system('sudo chmod 777 /var/www/html')
if val == 1:
    os.system('cp -rf index.html /var/www/html')
    os.system('cp -rf post.php /var/www/html')
    os.system('cp -rf static /var/www/html')
else:
    os.system('cp -rf ./html/* /var/www/html')
