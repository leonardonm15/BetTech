import os
import time
from main import main_procedure
from utilities.get_cookie import get_cookies
"""roda main.py a cada 40+ segundos. E a cada hora renova cookies rodando get_cookie.py"""

count = 0
while True:
    count += 40
    if count >= 60*60:
        get_cookies()
        time.sleep(60)
        main_procedure()
        count = 0
    else:
        main_procedure()
        time.sleep(60)

