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

    usernameInput = driver.find_element(By.ID, "txtUsername")
    usernameInput.send_keys("Midopazo")

    time.sleep(0.5)

    passwordInput = driver.find_element(By.ID, "txtPassword")
    passwordInput.send_keys("jppedrosaa")

    time.sleep(0.5)

    passwordInput.send_keys(Keys.RETURN)

    #continueButton = driver.find_element(By.CSS_SELECTOR, ".regulatory-last-login-modal__button")
    #continueButton.click()

    time.sleep(20)

    #switch to iframe
    #there are nested iframes

    outer_frame = driver.find_element(By.CLASS_NAME, 'inline-games-page-component__game-frame ')
    driver.switch_to.frame(outer_frame)

    inner_frame = driver.find_element(By.ID, 'gamecontent')
    driver.switch_to.frame(inner_frame)

    more_games = driver.find_element(By.CLASS_NAME, "header__more-games")
    more_games.click()

    time.sleep(0.5)

    multiple_rouletes = driver.find_element(By.CLASS_NAME, "lobby-category-item__icon_svg")
    multiple_rouletes.click()

    time.sleep(3)

    roulete_names_array = [element.text for element in driver.find_elements(By.CLASS_NAME, "lobby-table__name-container")]
    print(roulete_names_array)

    table_square = [element.get_attribute("innerHTML") for element in driver.find_elements(By.CLASS_NAME, "lobby-tables__item")]
    print(table_square[1][1320:1420]) #nesse html tem o nome da classe, tenta fazer um regex pra buscar uma string que começa com roulette-historyf, sim, com o f no final

    while True:
        pass
    #try:
    #    WebDriverWait(driver, 60).until(
    #        EC.element_to_be_clickable((By.CSS_SELECTOR, "#acrPopover > span.a-declarative > a"))).click()
    #finally:
    #    driver.quit()
    #moreGamesButton = driver.find_element(By.CLASS_NAME, "header__more-games")
    #moreGamesButton.click()

