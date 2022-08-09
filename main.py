from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver.v2 as uc
import time
import re 

if __name__ == '__main__':
    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    driver = uc.Chrome(options=options)
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

    #getting roulette class name
    table_square = [element.get_attribute("innerHTML") for element in driver.find_elements(By.CLASS_NAME, "lobby-tables__item")]
    to_search = table_square[1]
    roulette_class_name = re.search('roulette-historyf[^"]*', to_search).group(0).replace(" ", ".")

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


    for roulette in roulette_element_dic:
        roulette_counting_dic[roulette] = {
            "rua": 0,
            "canto": 0,
            "rua_dupla": 0,
            "dupla": 0,
            "zero": 0
        }
        # creating mask table for each roulette (used for checking patterns later)
        table = []
        for i in range(3):
            subtable = []
            for j in range(12):
                subtable.append(0)
            table.append(subtable)
        roulette_current_tables_dic[roulette] = table
        print(roulette)

        # initializing roulette_last_numbers_dic
        element_parent_of_numbers = roulette_element_dic[roulette].find_element(By.CLASS_NAME, roulette_class_name)
        print(element_parent_of_numbers.get_attribute("innerHTML"))
        all_roulette_number_elements = [element for element in element_parent_of_numbers.find_elements(By.TAG_NAME, "div")]
        print(all_roulette_number_elements)
        roulette_numbers = []
        # gets child of child of roulette number frame (where its actual number is)
        for i, number_element in enumerate(all_roulette_number_elements):
            if (i+1) % 3 != 0:
                continue
            # child_of_child = number_element.find_elements(By.TAG_NAME, "div")[1]
            if number_element.text == '':
                continue
            roulette_numbers.append(int(number_element.text))
        roulette_last_numbers_dic[roulette] = roulette_numbers
        print(roulette_numbers)

    #converting number to coordinate on roulette table
    def number_to_coordinate(num):
        num_tuple = (2-((number-1)%3), (number-1) // 3)
        return num_tuple

    # initializing roulette_current_tables_dic
    for roulette in roulette_last_numbers_dic:
        for number in roulette_last_numbers_dic[roulette]:
            # bomb bellow (don't know if this works 100%)
            if number == 0:
                roulette_counting_dic[roulette]["zero"] = 0
                continue
            roulette_current_tables_dic[roulette][2-((number-1)%3)][(number-1) // 3] = 1
            roulette_counting_dic[roulette]["zero"] += 1
        print(roulette, roulette_last_numbers_dic[roulette])
        for line in roulette_current_tables_dic[roulette]:
            print(line)

    #functions for pattern verification
    def verify_rua(roulette):
        first = roulette_last_numbers_dic[roulette][0]
        second = roulette_last_numbers_dic[roulette][1]
        third = roulette_last_numbers_dic[roulette][2]
        arr = [number_to_coordinate(first), number_to_coordinate(second), number_to_coordinate(third)]
        sorted_arr = sorted(arr)

        found = False
        if sorted_arr[0][0] == sorted_arr[1][0] and sorted_arr[1][0] == sorted_arr[2][0]:
            if sorted_arr[1][1] == sorted_arr[0][1]+1 and sorted_arr[2][1] == sorted_arr[1][1]+1:
                found = True
        return found

    def verify_dupla(roulette):
        first = roulette_last_numbers_dic[roulette][0]
        second = roulette_last_numbers_dic[roulette][1]
        arr = [number_to_coordinate(first), number_to_coordinate(second)]
        sorted_arr = sorted(arr)

        found = False
        if sorted_arr[0][0] == sorted_arr[1][0]:
            if sorted_arr[1][1] == sorted_arr[0][1] + 1:
                found = True
        elif sorted_arr[0][1] == sorted_arr[1][1]:
            if sorted_arr[1][0] == sorted_arr[0][0] + 1:
                found = True
        return found

    def verify_canto(roulette):
        first = roulette_last_numbers_dic[roulette][0]
        second = roulette_last_numbers_dic[roulette][1]
        third = roulette_last_numbers_dic[roulette][2]
        fourth = roulette_last_numbers_dic[roulette][3]
        arr = [number_to_coordinate(first), number_to_coordinate(second), number_to_coordinate(third), number_to_coordinate(fourth)]
        sorted_arr = sorted(arr)

        found = True
        if sorted_arr[1][0] != sorted_arr[0][0] or sorted_arr[1][1]-1 != sorted_arr[0][1]:
            found = False
        elif sorted_arr[2][1] != sorted_arr[0][1] or sorted_arr[1][0]-1 != sorted_arr[0][0]:
            found = False
        elif sorted_arr[3][1] != sorted_arr[1][1] or sorted_arr[3][0]-1 != sorted_arr[1][0]:
            found = False
        return found

    def verify_rua_dupla(roulette):
        first = roulette_last_numbers_dic[roulette][0]
        second = roulette_last_numbers_dic[roulette][1]
        third = roulette_last_numbers_dic[roulette][2]
        fourth = roulette_last_numbers_dic[roulette][3]
        fifth = roulette_last_numbers_dic[roulette][4]
        sixth = roulette_last_numbers_dic[roulette][5]
        arr = [number_to_coordinate(first), number_to_coordinate(second), number_to_coordinate(third), number_to_coordinate(fourth), number_to_coordinate(fifth), number_to_coordinate(sixth)]
        sorted_arr = sorted(arr)

        found1 = False
        if sorted_arr[0][0] == sorted_arr[1][0] and sorted_arr[1][0] == sorted_arr[2][0]:
            if sorted_arr[1][1] == sorted_arr[0][1]+1 and sorted_arr[2][1] == sorted_arr[1][1]+1:
                found1 = True
        found2 = False
        if sorted_arr[3][0] == sorted_arr[4][0] and sorted_arr[4][0] == sorted_arr[5][0]:
            if sorted_arr[4][1] == sorted_arr[3][1]+1 and sorted_arr[5][1] == sorted_arr[4][1]+1:
                found2 = True

        return found1 and found2

    # verifying
    while True:
        print("esperando 10 seg...")
        time.sleep(10)
        print("verificando...")
        for roulette in roulettes_needed:
            element_parent_of_numbers = roulette_element_dic[roulette].find_element(By.CLASS_NAME, roulette_class_name)
            all_roulette_number_elements = [element for element in
                                            element_parent_of_numbers.find_elements(By.TAG_NAME, "div")]
            numbers_to_compare = []
            for i, number_element in enumerate(all_roulette_number_elements):
                if (i + 1) % 3 != 0:
                    continue
                # child_of_child = number_element.find_elements(By.TAG_NAME, "div")[1]
                if number_element.text == '':
                    continue
                numbers_to_compare.append(int(number_element.text))
            if numbers_to_compare != roulette_last_numbers_dic[roulette]:
                # new number found
                for counter in roulette_counting_dic[roulette]:
                    roulette_counting_dic[roulette][counter] += 1

                new_number = numbers_to_compare[0]
                print(roulette, new_number)
                old_number = roulette_last_numbers_dic[roulette][len(roulette_last_numbers_dic[roulette]) - 1]
                # take old number off of mask
                roulette_current_tables_dic[roulette][2-((old_number-1)%3)][(old_number-1) // 3] = 0
                roulette_current_tables_dic[roulette][2-((new_number-1)%3)][(new_number-1) // 3] = 1
                roulette_last_numbers_dic[roulette] = numbers_to_compare
                #verify for patterns
                if new_number == 0:
                    roulette_counting_dic[roulette]["zero"] = 0
                if verify_rua(roulette):
                    roulette_counting_dic[roulette]["rua"] = 0
                if verify_canto(roulette):
                    roulette_counting_dic[roulette]["canto"] = 0
                if verify_dupla(roulette):
                    roulette_counting_dic[roulette]["dupla"] = 0
                if verify_rua_dupla(roulette):
                    roulette_counting_dic[roulette]["rua_dupla"] = 0
        print("verificou")
