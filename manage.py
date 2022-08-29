import os
import time
import pathlib
import platform

current_path = str(pathlib.Path().resolve()) + "/"
makingjson_path = '/data/makingjson.py'
cookie_path = '/utilities/get_cookie.py'
main_path = '/main.py'
if platform.system() == 'Windows':
    current_path = str(pathlib.Path().resolve())
    cookie_path = current_path + cookie_path
    main_path = current_path + main_path
    makingjson_path = current_path + makingjson_path

os.system(f'python {makingjson_path}')
count = 0
while True:
    count += 40
    if count >= 60*60:
        count = 0
        print('me acha')
        os.system(f'python {cookie_path}')
        time.sleep(40)
        os.system(f'python {main_path}')
        time.sleep(40)
    else:
        os.system(f'python {main_path}')
        time.sleep(40)
