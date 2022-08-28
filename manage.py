import os
import time
"""roda main.py a cada 40+ segundos. E a cada hora renova cookies rodando get_cookie.py"""

if __name__ == '__main__':
    os.system("python3 data/makingjson.py")
    count = 0
    while True:
        count += 40
        if count == 40 or count >= 60*60:
            #os.system("python3 utilities/get_cookie.py")
            time.sleep(10)
            os.system("python3 main.py")
            count = 0
        else:
            os.system("python3 main.py")
        time.sleep(40)

