from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver.v2 as uc
import time
import re 

if __name__ == '__main__':

    driver = uc.Chrome()
    driver.get("https://livecasino.bet365.com/Play/LiveRoulette")

    usernameInput = driver.find_element(By.ID, "txtUsername")
    usernameInput.send_keys("ninjadocassino")

    time.sleep(0.5)

    passwordInput = driver.find_element(By.ID, "txtPassword")
    passwordInput.send_keys("cassino")

    time.sleep(0.5)

    passwordInput.send_keys(Keys.RETURN)

    #continueButton = driver.find_element(By.CSS_SELECTOR, ".regulatory-last-login-modal__button")
    #continueButton.click()

    time.sleep(40)

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

    table_square = [element.get_attribute("innerHTML") for element in driver.find_elements(By.CLASS_NAME, "lobby-tables__item")]
    to_search = table_square[1]

    #getting roulette class name
    begin_of_class_name = to_search.find('roulette-historyf')
    end_of_class_name = 0
    for i, e in enumerate(to_search[begin_of_class_name:len(to_search)]):
        if e == ' ':
            end_of_class_name = i + begin_of_class_name
            break
    roulette_class_name = to_search[begin_of_class_name:end_of_class_name + 1]

    # to-do: verify if these are the actual numbers of needed roulettes
    roulettes_needed = ["Roulette", "Football Roulette", "Hindi Roulette", "Speed Roulette", "Greek Roulette", "Turkish Roulette", "Roleta Brasileira", "Prestige Roulette", "Nederlandstalige Roulette", "Deutsches Roulette", "UK Roulette", "Bucharest Roulette", "Roulette Italiana"]
    roulette_element_dic = {}
    roulette_counting_dic = {}
    roulette_last_numbers_dic = {}
    roulette_current_tables_dic = {}

    roulete_names_array = [element.text for element in driver.find_elements(By.CLASS_NAME, "lobby-table__name-container")]
    all_roulettes = [element for element in driver.find_elements(By.CLASS_NAME, "lobby-table__name-container")]
    for element in all_roulettes:
        if element.text in roulettes_needed:
            # gets parent of parent (whole roulette frame)
            roulette_element_dic[element.text] = (element.find_element(By.XPATH, '..')).find_element(By.XPATH, '..')
    roulette_all_numbers_array = [element.find_elements(By.TAG_NAME, "div") for element in driver.find_elements(By.CLASS_NAME, roulette_class_name)]

    # creating mask table for each roulette (used for checking patterns later)
    table = []
    for i in range(3):
        subtable = []
        for j in range(12):
            subtable.append(0)
        table.append(subtable)

    for roulette in roulette_element_dic:
        roulette_counting_dic[roulette] = 0
        roulette_current_tables_dic[roulette] = table

        # initializing roulette_last_numbers_dic
        all_roulette_number_elements = [element for element in roulette_element_dic[roulette].find_element(By.CLASS_NAME, roulette_class_name)]
        roulette_numbers = []
        # gets child of child of roulette number frame (where its actual number is)
        for number_element in all_roulette_number_elements:
            child = number_element.find_element(By.TAG_NAME, "div")
            child_of_child = child.find_element(By.TAG_NAME, "div")
            roulette_numbers.append(int(child_of_child.text))
        roulette_last_numbers_dic[roulette] = roulette_numbers

    # initializing roulette_current_tables_dic
    for roulette in roulette_last_numbers_dic:
        for number in roulette_last_numbers_dic[roulette]:
            # bomb bellow (don't know if this works 100%)
            roulette_current_tables_dic[roulette][number // 12][number % 12] = 1

    # defining verifying functions (NEEDS CHANGES)
    def verify_rua(t, i, j):
        rua = True
        for x in range(3):
            if tables[t][x][j] == 0:
                rua = False
        return rua
    
    def verify_dupla(t, i, j):
        dupla = False 
        if i > 0:
            if tables[t][i-1][j] == 1:
                dupla = True
        if j > 0: 
            if tables[t][i][j-1] == 1:
                dupla = True
        if i < 2: 
            if tables[t][i+1][j] == 1:
                dupla = True
        if j < 11: 
            if tables[t][i][j+1] == 1:
                dupla = True
        return dupla

    # verifying
    while True:
        time.sleep(10)


    #try:
    #    WebDriverWait(driver, 60).until(
    #        EC.element_to_be_clickable((By.CSS_SELECTOR, "#acrPopover > span.a-declarative > a"))).click()
    #finally:
    #    driver.quit()
    #moreGamesButton = driver.find_element(By.CLASS_NAME, "header__more-games")
    #moreGamesButton.click()

