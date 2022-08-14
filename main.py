import time
import re
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc

sys.path.insert(0, r"SuperBetTech\utilities")
sys.path.insert(0, r"SuperBetTech\bot_tlg")

from utilities.pattern_verification import pattern_verification
from utilities.update_last_numbers import update_last_numbers

if __name__ == '__main__':
    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get("https://livecasino.bet365.com/Play/LiveRoulette")

    # logar
    usernameInput = driver.find_element(By.ID, "txtUsername")
    usernameInput.send_keys("Midopazo")

    time.sleep(0.5)

    passwordInput = driver.find_element(By.ID, "txtPassword")
    passwordInput.send_keys("jppedrosaa")

    time.sleep(0.5)

    passwordInput.send_keys(Keys.RETURN)

    # continueButton = driver.find_element(By.CSS_SELECTOR, ".regulatory-last-login-modal__button")
    # continueButton.click()

    time.sleep(30)

    # switch to iframe
    # there are nested iframes

    outer_frame = driver.find_element(By.CLASS_NAME, 'inline-games-page-component__game-frame ')
    driver.switch_to.frame(outer_frame)

    inner_frame = driver.find_element(By.ID, 'gamecontent')
    driver.switch_to.frame(inner_frame)

    more_games = driver.find_element(By.CLASS_NAME, "more-games-buttonN0Yt8ztSf1nWOgXO5ftu")
    more_games.click()

    time.sleep(0.5)

    multiple_rouletes = driver.find_element(By.CLASS_NAME, "lobby-category-item__icon_svg")
    multiple_rouletes.click()

    time.sleep(3)

    # getting roulette class name
    table_square = [element.get_attribute("innerHTML") for element in
                    driver.find_elements(By.CLASS_NAME, "lobby-tables__item")]
    to_search = table_square[1]
    roulette_class_name = re.search('roulette-historyf[^"]*', to_search).group(0).replace(" ", ".")

    # to-do: verify if these are the actual numbers of needed roulettes
    roulettes_needed = ["Roulette", "Football Roulette", "Hindi Roulette", "Speed Roulette", "Greek Roulette",
                        "Turkish Roulette", "Roleta Brasileira", "Prestige Roulette", "Nederlandstalige Roulette",
                        "Deutsches Roulette", "UK Roulette", "Bucharest Roulette", "Roulette Italiana"]
    roulette_element_dic = {}

    all_roulettes = [element for element in driver.find_elements(By.CLASS_NAME, "lobby-table__name-container")]
    for element in all_roulettes:
        if element.text in roulettes_needed:
            # gets parent of parent (whole roulette frame)
            roulette_element_dic[element.text] = (element.find_element(By.XPATH, '..')).find_element(By.XPATH, '..')

    for roulette in roulette_element_dic:
        # initializing roulette_last_numbers_dic
        element_parent_of_numbers = roulette_element_dic[roulette].find_element(By.CLASS_NAME, roulette_class_name)
        all_roulette_number_elements = [element for element in
                                       element_parent_of_numbers.find_elements(By.TAG_NAME, "div")]
        print(f"numero de todas as roletas -> {[element.text for element in all_roulette_number_element]}")
        roulette_numbers = []
        # gets child of child of roulette number frame (where its actual number is)
        for i, number_element in enumerate(all_roulette_number_elements):
            if (i + 1) % 3 != 0:
                continue
            # child_of_child = number_element.find_elements(By.TAG_NAME, "div")[1]
            if number_element.text == '':
                continue
            roulette_numbers.append(int(number_element.text))
        new_numbers = update_last_numbers(roulette, roulette_numbers)
        for number in new_numbers:
            pattern_verification(roulette, number)
