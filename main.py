from typing import Any

import time
import re
import sys
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc

sys.path.insert(0, r"SuperBetTech\utilities")
sys.path.insert(0, r"SuperBetTech\bot_tlg")

from utilities.pattern_verification import pattern_verification
from utilities.update_last_numbers import update_last_numbers
from data import *

data = open('data/data.json')
info_json = json.load(data)

options = uc.ChromeOptions()
# options.add_argument('--headless')
driver = uc.Chrome(options=options)
driver.get("https://livecasino.bet365.com/Play/LiveRoulette")


roulette_historic_match_name = []
roulettes_needed = ["Roulette", "Football Roulette", "Hindi Roulette", "Speed Roulette", "Greek Roulette",
                    "Turkish Roulette", "Roleta Brasileira", "Prestige Roulette", "Nederlandstalige Roulette",
                    "Deutsches Roulette", "UK Roulette", "Bucharest Roulette", "Roulette Italiana"]

if __name__ == '__main__':
    # logar
    usernameInput = driver.find_element(By.ID, "txtUsername")
    usernameInput.send_keys("Midopazo")

    time.sleep(0.5)

    passwordInput = driver.find_element(By.ID, "txtPassword")
    passwordInput.send_keys("jppedrosaa")

    time.sleep(0.5)

    passwordInput.send_keys(Keys.RETURN)

    time.sleep(30)

    # switch to iframes
    outer_frame = driver.find_element(By.CLASS_NAME, 'inline-games-page-component__game-frame ')
    driver.switch_to.frame(outer_frame)

    inner_frame = driver.find_element(By.ID, 'gamecontent')
    driver.switch_to.frame(inner_frame)

    #click more frames
    more_games = driver.find_element(By.CLASS_NAME, "more-games-buttonN0Yt8ztSf1nWOgXO5ftu")
    more_games.click()

    time.sleep(0.5)

    #click multiple roletes
    multiple_rouletes = driver.find_element(By.CLASS_NAME, "lobby-category-item__icon_svg")
    multiple_rouletes.click()

    time.sleep(3)

    # getting roulette class name, find the elements and assemble the historic array
    # '33\n21\n8\n2\n18\n21\n32\n9\n22\n11' <- the way that the historic comes out of the html
    table_square = [element.get_attribute("innerHTML") for element in
                    driver.find_elements(By.CLASS_NAME, "lobby-tables__item")]
    to_search = table_square[1]
    roulette_class_name = re.search('roulette-historyf[^"]*', to_search).group(0).replace(" ", ".")
    # formating '33\n21\n8\n2\n18\n21\nx32\n9\n22\n11' to "33", "21", "x32"
    number_historic_arrays = [elements.text.replace("x", "-").split("\n") for elements in
                              driver.find_elements(By.CLASS_NAME, roulette_class_name)]
    number_historic_arrays = [[int(number) for number in array] for array in number_historic_arrays]

    # get the multipliers out, like x120 or x37
    for historico in number_historic_arrays:
        c = -1
        for numero in historico:
            c += 1
            if numero < 0:
                print(f'numero popado {historico[c]}')
                historico.pop(c)

    print(f"arrays com historico das roletas {number_historic_arrays}")

    all_roulettes_names = [element.text for element in driver.find_elements(By.CLASS_NAME, "lobby-table__name-container")]

    print(f"o numero de historicos é {len(number_historic_arrays)} e o numero de nome de roletas é {len(all_roulettes_names)}")

    c = -1
    for roulette_name in all_roulettes_names:
        c += 1
        if roulette_name in roulettes_needed:
            roulette_historic_match_name.append((roulette_name, number_historic_arrays[c]))

    for group in roulette_historic_match_name:
        # group comes like that -. ("roulette name", [extracted numbers])
        new_numbers = update_last_numbers(info_json[group[0]], group[1])
        for number in new_numbers:
            pattern_verification(info_json[group[0], group[1]])

        #to-do quando o historico estiver vazio preencher ele com os numeros que vierem do rolette historic match

    while True:
        pass
