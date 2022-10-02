# -*- coding: utf-8 -*-

import time
import re
import json
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
# sys.path.insert(0, r"SuperBetTech\utilities")
# sys.path.insert(0, r"SuperBetTech\bot_tlg")
from utilities.pattern_verification import pattern_verification
from utilities.update_last_numbers import update_last_numbers
import tlg
from utilities.conversions import *

roulette_historic_match_name = []
bot_tlg = tlg.BotTlg()

roulettes_needed = ["Roulette", "Football Roulette", "Hindi Roulette", "Speed Roulette", "Greek Roulette",
                    "Turkish Roulette", "Roleta Brasileira", "Prestige Roulette", "Nederlandstalige Roulette",
                    "Deutsches Roulette", "UK Roulette", "Bucharest Roulette", "Roulette Italiana"]

if __name__ == '__main__':
    data = open('data/data.json')
    info_json = json.load(data)

    data_config = open('data/config.json')
    info_config = json.load(data_config)

    cookies_data = open("data/cookies.JSON")
    cookies = json.load(cookies_data)
    print(cookies)

    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, cookies=cookies)
    driver.get("https://livecasino.bet365.com/Play/LiveRoulette")

    for cookie in cookies:
        driver.add_cookie({"name": cookie, "value": cookies[cookie]})
    driver.refresh()

    time.sleep(30)

    # switch to iframes
    try:
        random_ok_button = driver.find_element(By.CLASS_NAME, "modal-footer-btn modal-footer-btn_resolve modal-footer-btn_full")
        print("trying")
    except:
        print("except")
        outer_frame = driver.find_element(By.CLASS_NAME, 'inline-games-page-component__game-frame')
        driver.switch_to.frame(outer_frame)
        inner_frame = driver.find_element(By.ID, 'gamecontent')
        driver.switch_to.frame(inner_frame)

        more_games = driver.find_element(By.CLASS_NAME, "more-games-buttonN0Yt8ztSf1nWOgXO5ftu")
        more_games.click()
    else:
        print("else")
        random_ok_button.click()

    time.sleep(0.5)

    # click multiple roletes
    multiple_rouletes = driver.find_element(By.CLASS_NAME, "lobby-category-item__icon_svg")
    multiple_rouletes.click()

    time.sleep(3)

    table_square = [element.get_attribute("innerHTML") for element in
                    driver.find_elements(By.CLASS_NAME, "lobby-tables__item")]
    to_search = table_square[1]
    roulette_class_name = re.search('roulette-historyf[^"]*', to_search).group(0).replace(" ", ".")

    number_historic_arrays = [elements.text.replace("x", "-").split("\n") for elements in
                              driver.find_elements(By.CLASS_NAME, roulette_class_name)]
    number_historic_arrays = [[int(number) for number in array] for array in number_historic_arrays]

    for historico in number_historic_arrays:
        c = -1
        for numero in historico:
            c += 1
            if numero < 0:
                historico.pop(c)

    all_roulettes_names = [element.text for element in
                           driver.find_elements(By.CLASS_NAME, "lobby-table__name-container")]

    #corrigindo caso haja roletas "bonus"
    while len(number_historic_arrays) != len(all_roulettes_names):
        if len(number_historic_arrays) < len(all_roulettes_names):
            all_roulettes_names.pop(0)
        else:
            number_historic_arrays.pop(0)

    c = -1
    for roulette_name in all_roulettes_names:
        c += 1
        if roulette_name in roulettes_needed:
            roulette_historic_match_name.append((roulette_name, number_historic_arrays[c]))

    # verificação de padrões junto com reconhecimento de novos numeros
    for group in roulette_historic_match_name:
        # group comes like that -. ("roulette name", [extracted numbers])
        # print("info_json[group[0]]['numbers']: ", info_json[group[0]]['numbers'])
        # print("group[1]: ", group[1])
        new_numbers = update_last_numbers(info_json[group[0]]['numbers'], group[1])

        for number in new_numbers:
            pattern_verification(group[0], number, info_json)
        info_json[group[0]]['numbers'] = group[1]

        print(group[0], new_numbers)

        # print(new_numbers)
        roulette = group[0]
        for pattern in info_json[roulette]["patterns"]:
            if info_config[pattern] == 0 and pattern != "direta":
                # padrao esta desligado
                continue
            if pattern == "canto":
                verify = [[0 for _ in range(11)] for _ in range(2)]
                for i, arr in enumerate(info_json[roulette]["patterns"][pattern]):
                    for j in range(len(arr)):
                        nums = convert_canto_pos_to_nums(i, j)
                        find_num = next((h for h, x in enumerate(new_numbers) if
                                         x == nums[0] or x == nums[1] or x == nums[2] or x == nums[3]), -1)
                        if find_num == -1:
                            arr[j] += len(new_numbers)
                        else:
                            arr[j] += find_num
            elif pattern == "dupla":
                for direction in info_json[roulette]["patterns"][pattern]:
                    for i, arr in enumerate(info_json[roulette]["patterns"][pattern][direction]):
                        for j in range(len(arr)):
                            num = convert_direta_pos_to_num(i, j)
                            if direction == 'right':
                                num2 = num + 3
                            else:
                                num2 = num - 1
                            find_num = next((h for h, x in enumerate(new_numbers) if x == num or x == num2), -1)
                            if find_num == -1:
                                arr[j] += len(new_numbers)
                            else:
                                arr[j] += find_num
            elif pattern == "direta":
                for i in range(len(info_json[roulette]["patterns"][pattern])):
                    find_num = next((j for j, x in enumerate(new_numbers) if x == i), -1)
                    if find_num == -1:
                        info_json[roulette]["patterns"][pattern][i] += len(new_numbers)
                    else:
                        info_json[roulette]["patterns"][pattern][i] += find_num
            elif pattern == "rua":
                for i in range(len(info_json[roulette]["patterns"][pattern])):
                    find_num = next((j for j, x in enumerate(new_numbers) if i * 3 + 3 >= x >= i * 3 + 1), -1)
                    if find_num == -1:
                        info_json[roulette]["patterns"][pattern][i] += len(new_numbers)
                    else:
                        info_json[roulette]["patterns"][pattern][i] += find_num
            elif pattern == "rua_dupla":
                for i in range(len(info_json[roulette]["patterns"][pattern])):
                    find_num = next((j for j, x in enumerate(new_numbers) if i * 3 + 6 >= x >= i * 3 + 1), -1)
                    if find_num == -1:
                        info_json[roulette]["patterns"][pattern][i] += len(new_numbers)
                    else:
                        info_json[roulette]["patterns"][pattern][i] += find_num

    with open("./data/data.json", "w") as write_file:
        json.dump(info_json, write_file, indent=4)

    #verify things to see if it has to send some message
    for roulette in info_json:
        last_number = info_json[roulette]['numbers'][0]
        # verificar dupla
        if info_config["dupla"] == 1:
            matriz_dupla_aviso_right = info_json[roulette]["avisos"]["dupla"]["right"]
            matriz_dupla_right = info_json[roulette]["patterns"]["dupla"]["right"]
            for i, arr_dupla_right in enumerate(matriz_dupla_right):
                for j, num_dupla_right in enumerate(arr_dupla_right):
                    if num_dupla_right >= 64:
                        if num_dupla_right <= 64+17:
                            bot_tlg.alerta_dupla(i, j, "right", num_dupla_right, roulette, last_number)
                    else:
                        matriz_dupla_aviso_right[i][j] = 0
            matriz_dupla_aviso_down = info_json[roulette]["avisos"]["dupla"]["down"]
            matriz_dupla_down = info_json[roulette]["patterns"]["dupla"]["down"]
            for i, arr_dupla_down in enumerate(matriz_dupla_down):
                for j, num_dupla_down in enumerate(arr_dupla_down):
                    if num_dupla_down >= 64:
                        if num_dupla_down <= 64+17:
                            bot_tlg.alerta_dupla(i, j, "down", num_dupla_down, roulette, last_number)

        # verificar canto
        if info_config["canto"] == 1:
            matriz_canto_aviso = info_json[roulette]["avisos"]["canto"]
            matriz_canto = info_json[roulette]["patterns"]["canto"]
            for i, arr_canto in enumerate(matriz_canto):
                for j, num in enumerate(arr_canto):
                    if num >= 43:
                        if num <= 43+8:
                            bot_tlg.alerta_canto(i, j, num, roulette, last_number)

        # verificar rua
        if info_config["rua"] == 1:
            arr_rua_aviso = info_json[roulette]["avisos"]["rua"]
            arr_rua = info_json[roulette]["patterns"]["rua"]
            for i, num in enumerate(arr_rua):
                if num >= 37:
                    if num <= 38:
                        bot_tlg.alerta_rua(i, num, roulette, last_number)

        # verificar rua dupla (necessita de uns ajustes)
        if info_config["rua_dupla"] == 1:
            arr_rua_dupla_aviso = info_json[roulette]["avisos"]["rua_dupla"]
            arr_rua_dupla = info_json[roulette]["patterns"]["rua_dupla"]
            for i, num in enumerate(arr_rua_dupla):
                if num >= 20:
                    if not arr_rua_dupla_aviso[i]:
                        bot_tlg.alerta_rua_dupla(i, num, roulette, last_number)
                        arr_rua_dupla_aviso[i] = 1
                else:
                    arr_rua_dupla_aviso[i] = 0

        # verificar direta
        if info_config["direta"] == 1:
            arr_direta_aviso = info_json[roulette]["avisos"]["direta"]
            arr_direta = info_json[roulette]["patterns"]["direta"]
            for i, num in enumerate(arr_direta):
                if num >= 128:
                    if not arr_direta_aviso[i]:
                        bot_tlg.alerta_direta(i, num, roulette, last_number)
                        arr_direta_aviso[i] = 1
                else:
                    arr_direta_aviso[i] = 0

        # verificacao "agrupamento do zero"
        if info_config["agrupamento"] == 1:
            arr_direta = info_json[roulette]["patterns"]["direta"]
            avisar = True
            agrupamento_zero = [12, 35, 3, 26, 0, 32, 15]
            menor_num = 10000000
            for num in agrupamento_zero:
                menor_num = min(arr_direta[num], menor_num)
                if arr_direta[num] < 14:
                    avisar = False
            if avisar:
                if menor_num <= 14+4:
                    bot_tlg.alerta_do_zero(menor_num, roulette, last_number)

    print(bot_tlg.mensagem)
    bot_tlg.send_message()

    # print(info_json)
    with open("./data/data.json", "w") as write_file:
        json.dump(info_json, write_file, indent=4)
    c = 0

    driver.quit()
