import os
import time
import pathlib
import platform

current_path = str(pathlib.Path().resolve()) + "/"
print(current_path)
makingjson_path = 'data/makingjson.py'
cookie_path = 'utilities/get_cookie.py'
main_path = 'main.py'
if platform.system() == 'Windows':
    current_path = str(pathlib.Path().resolve())
    cookie_path = current_path + cookie_path
    main_path = current_path + main_path
    makingjson_path = current_path + makingjson_path

os.system(f'python3 {makingjson_path}')

count = 0
while True:
    count += 40
    if count >= 60*60:
        os.system(f'python3 {cookie_path}')
        time.sleep(60)
        os.system(f'python3 {main_path}')
        count = 0
    else:
        time.sleep(40)
        os.system(f'python3 {main_path}')

