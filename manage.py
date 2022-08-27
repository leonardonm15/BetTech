import os
import time

"""roda main.py a cada 40+ segundos. E a cada hora renova cookies rodando get_cookie.py"""

count = 0
os.system("python3 ./data/makingjson.py")
os.system("python3 ./utilities/get_cookie.py")
print("hello")
while True:
    count += 40
    if count >= 60*60:
        os.system("python3 ./utilities/get_cookie.py")
        time.sleep(60)
        os.system("python3 main.py")
        count = 0
    else:
        time.sleep(40)
        os.system("python3 main.py")
