from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver.v2 as uc
import time

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.get("https://livecasino.bet365.com/Play/LiveRoulette")
    print(driver.__dict__)
    print(dir(driver))
    usernameInput = driver.find_element(By.ID, "txtUsername")
    usernameInput.send_keys("ninjadocassino")
    passwordInput = driver.find_element(By.ID, "txtPassword")
    passwordInput.send_keys("cassino")
    passwordInput.send_keys(Keys.RETURN)
    time.sleep(30)
    continueButton = driver.find_element(By.CSS_SELECTOR, ".regulatory-last-login-modal__button")
    continueButton.click()
    time.sleep(30)
    elem = driver.find_element(By.CLASS_NAME, "inline-games-page-component__game-header-right ")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, -70, 40)
    action.click()
    action.perform()
    time.sleep(10)
    action.move_to_element_with_offset(elem, -737, 127)
    action.click()
    action.perform()
    time.sleep(10)
    print(driver.page_source())
    while True:
        pass
    #try:
    #    WebDriverWait(driver, 60).until(
    #        EC.element_to_be_clickable((By.CSS_SELECTOR, "#acrPopover > span.a-declarative > a"))).click()
    #finally:
    #    driver.quit()
    #moreGamesButton = driver.find_element(By.CLASS_NAME, "header__more-games")
    #moreGamesButton.click()

