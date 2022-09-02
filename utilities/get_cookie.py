from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
import time
import json


cookies = {}

if __name__ == '__main__':
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.get("https://livecasino.bet365.com/Play/LiveRoulette")

    time.sleep(0.5)
    usernameInput = driver.find_element(By.ID, "txtUsername")
    usernameInput.send_keys("doidodocassino")
    time.sleep(0.5)
    passwordInput = driver.find_element(By.ID, "txtPassword")
    passwordInput.send_keys("cassino")
    time.sleep(0.5)
    passwordInput.send_keys(Keys.RETURN)

    time.sleep(5)
    cookies_array = driver.get_cookies()
    for cookie in cookies_array:
        cookies[cookie['name']] = cookie['value']

    with open('./data/cookies.JSON', 'w') as wf:
        json.dump(cookies, wf)

    driver.close()
