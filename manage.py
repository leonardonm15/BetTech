import os
import time
from main import main_procedure
import os
import time

"""roda main.py a cada 40+ segundos. E a cada hora renova cookies rodando get_cookie.py"""

count = 0
get_cookie_path = pathlib.Path().resolve("C:\Users\Leona\PycharmProjects\SuperBetTech\utilities\get_cookie.py")
get_main_path = pathlib.Path().resolve("C:\Users\Leona\PycharmProjects\SuperBetTech\main.py")
#os.system("./data/makingjson.py")
#os.system("./utilities/get_cookie.py")
print("hello")
while True:
    count += 40
    if count >= 60*60:
        os.system(get_cookie_path)
        time.sleep(60)
        os.system(get_main_path)
        count = 0
    else:
        time.sleep(40)
        os.system(get_main_path)

