import os
import time
import pathlib
import platform

current_path = str(pathlib.Path().resolve()) + "/"
makingjson_path = 'data/makingjson.py'
cookie_path = 'utilities/get_cookie.py'
main_path = 'main.py'
python_command = ""
if platform.system() == 'Windows':
    python_command = "python"
    makingjson_path = '/data/makingjson.py'
    cookie_path = '/utilities/get_cookie.py'
    main_path = '/main.py'
    current_path = str(pathlib.Path().resolve())
    cookie_path = current_path + cookie_path
    main_path = current_path + main_path
    makingjson_path = current_path + makingjson_path
else:
    python_command = "python3"

os.system(f'{python_command} {makingjson_path}')
count = 0
while True:
    count += 40
    if count >= 60*60 or count == 40:
        count = 0
        print('me acha')
        os.system(f'{python_command} {cookie_path}')
        time.sleep(40)
        os.system(f'{python_command} {main_path}')
        time.sleep(40)
    else:
        os.system(f'{python_command} {main_path}')
        time.sleep(40)
