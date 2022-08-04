from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
import time

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.get("https://livecasino.bet365.com/Play/LiveRoulette")
    usernameInput = driver.find_element(By.ID, "txtUsername")
    usernameInput.send_keys("ninjadocassino")
    passwordInput = driver.find_element(By.ID, "txtPassword")
    passwordInput.send_keys("cassino")
    passwordInput.send_keys(Keys.RETURN)
    time.sleep(60)
    continueButton = driver.find_element(By.CLASS_NAME, "regulatory-last-login-modal__button")
    continueButton.click()
    time.sleep(60)
    moreGamesButton = driver.find_element(By.CLASS_NAME, "header__more-games")
    moreGamesButton.click()

