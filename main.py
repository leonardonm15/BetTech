import time
import telegram
import dotenv
import os
import re
import sys
import json
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
# sys.path.insert(0, r"SuperBetTech\utilities")
# sys.path.insert(0, r"SuperBetTech\bot_tlg")
from utilities.pattern_verification import pattern_verification
from utilities.update_last_numbers import update_last_numbers
from bot_tlg import tlg

roulette_historic_match_name = []
bot_tlg = tlg.BotTlg()
roulettes_needed = ["Roulette", "Football Roulette", "Hindi Roulette", "Speed Roulette", "Greek Roulette",
                    "Turkish Roulette", "Roleta Brasileira", "Prestige Roulette", "Nederlandstalige Roulette",
                    "Deutsches Roulette", "UK Roulette", "Bucharest Roulette", "Roulette Italiana"]

def main_procedure():
    if __name__ == '__main__':
        freeze_support()
        data = open('/data/data.json')
        info_json = json.load(data)

        cookies_data = open("/data/cookies.JSON")
        cookies = json.load(cookies_data)

        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options, cookies=cookies)
        driver.get("https://livecasino.bet365.com/Play/LiveRoulette")

        for cookie in cookies:
            print(cookie, cookies[cookie])
            driver.add_cookie({"name": cookie, "value": cookies[cookie]})
        driver.refresh()

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

        #while True:
        data = open('data/data.json')
        info_json = json.load(data)

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

        #verificação de padrões junto com reconhecimento de novos numeros
        for group in roulette_historic_match_name:
            # group comes like that -. ("roulette name", [extracted numbers])
            print("roulette: ", group[0])
            print("info_json[group[0]]['numbers']: ", info_json[group[0]]['numbers'])
            print("group[1]: ", group[1])
            new_numbers = update_last_numbers(info_json[group[0]]['numbers'], group[1])

            print(new_numbers)
            roulette = group[0]
            for pattern in info_json[roulette]["patterns"]:
                if pattern == "canto":
                    for arr in info_json[roulette]["patterns"][pattern]:
                        for i in range(len(arr)):
                            arr[i] += len(new_numbers)
                elif pattern == "dupla":
                    for direction in info_json[roulette]["patterns"][pattern]:
                        for arr in info_json[roulette]["patterns"][pattern][direction]:
                            for i in range(len(arr)):
                                arr[i] += len(new_numbers)
                else:
                    for i in range(len(info_json[roulette]["patterns"][pattern])):
                        info_json[roulette]["patterns"][pattern][i] += len(new_numbers)

            for number in new_numbers:
                pattern_verification(group[0], number, info_json)
            info_json[group[0]]['numbers'] = group[1]


        for roulette in info_json:
            # verificar dupla
            matriz_dupla_aviso_right = info_json[roulette]["avisos"]["dupla"]["right"]
            matriz_dupla_right = info_json[roulette]["patterns"]["dupla"]["right"]
            for i, arr_dupla_right in enumerate(matriz_dupla_right):
                for j, num_dupla_right in enumerate(arr_dupla_right):
                    if num_dupla_right >= 64:
                        if not matriz_dupla_aviso_right[i][j]:
                            bot_tlg.alerta_dupla(i, j, "right", num_dupla_right, roulette, roulette['numbers'][0])
                            matriz_dupla_aviso_right[i][j] = 1
                    else:
                        matriz_dupla_aviso_right[i][j] = 0
            matriz_dupla_aviso_down = info_json[roulette]["avisos"]["dupla"]["down"]
            matriz_dupla_down = info_json[roulette]["patterns"]["dupla"]["down"]
            for i, arr_dupla_down in enumerate(matriz_dupla_down):
                for j, num_dupla_down in enumerate(arr_dupla_down):
                    if num_dupla_down >= 64:
                        if not matriz_dupla_aviso_down[i][j]:
                            bot_tlg.alerta_dupla(i, j, "down", num_dupla_down, roulette, roulette['numbers'][0])
                            matriz_dupla_aviso_down[i][j] = 1
                    else:
                        matriz_dupla_aviso_down[i][j] = 0


            # verificar canto
            matriz_canto_aviso = info_json[roulette]["avisos"]["canto"]
            matriz_canto = info_json[roulette]["patterns"]["canto"]
            for i, arr_canto in enumerate(matriz_canto):
                for j, num in enumerate(arr_canto):
                    if num >= 35:
                        if not matriz_canto_aviso[i][j]:
                            bot_tlg.alerta_canto(i, j, num, roulette, roulette['numbers'][0])
                            matriz_canto_aviso[i][j] = 1
                    else:
                        matriz_canto_aviso[i][j] = 0

            # verificar rua
            arr_rua_aviso = info_json[roulette]["avisos"]["rua"]
            arr_rua = info_json[roulette]["patterns"]["rua"]
            for i, num in enumerate(arr_rua):
                if num >= 35:
                    if not arr_rua_aviso[i]:
                        bot_tlg.alerta_rua(i, num, roulette, roulette['numbers'][0])
                        arr_rua_aviso[i] = 1
                else:
                    arr_rua_aviso[i] = 0

            # verificar rua dupla
            arr_rua_dupla_aviso = info_json[roulette]["avisos"]["rua_dupla"]
            arr_rua_dupla = info_json[roulette]["patterns"]["rua_dupla"]
            for i, num in enumerate(arr_rua_dupla):
                if num >= 20:
                    if not arr_rua_dupla_aviso[i]:
                        bot_tlg.alerta_rua_dupla(i, num, roulette, roulette['numbers'][0])
                        arr_rua_dupla_aviso[i] = 1
                else:
                    arr_rua_dupla_aviso[i] = 0

            # verificar direta
            arr_direta_aviso = info_json[roulette]["avisos"]["direta"]
            arr_direta = info_json[roulette]["patterns"]["direta"]
            for i, num in enumerate(arr_direta):
                if num >= 128:
                    if not arr_direta_aviso[i]:
                        bot_tlg.alerta_direta(i, num, roulette, roulette['numbers'][0])
                        arr_direta_aviso[i] = 1
                else:
                    arr_direta_aviso[i] = 0

            #verificacao "agrupamento do zero"
            avisar = True
            agrupamento_zero = [12, 35, 3, 26, 0, 32, 15]
            menor_num = 10000000
            for num in agrupamento_zero:
                menor_num = min(arr_direta[num], menor_num)
                if arr_direta[num] < 15:
                    avisar = False
            if avisar:
                bot_tlg.alerta_do_zero(menor_num, roulette, roulette['numbers'][0])

        print(bot_tlg.mensagem)

        print(info_json)
        with open("./data/data.json", "w") as write_file:
            json.dump(info_json, write_file, indent=4)
        c = 0
