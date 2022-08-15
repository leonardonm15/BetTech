import json
data_file = open("data/data.JSON")
data = json.load(data_file)


def update_rua(roulette, new_number):
    index = (new_number-1)//3
    data[roulette]["patterns"]["rua"][index] = 0


def uptade_rua_dupla(roulette, new_number):
    index = (new_number-1)//3
    if index > 0:
        data[roulette]["patterns"]["rua_dupla"][index-1] = 0

    if index < 10:
        data[roulette]["patterns"]["rua_dupla"][index+1] = 0


def update_canto(roulette, new_number):
    is_corner = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    moves = [[0, 0], [0, -1], [-1, 0], [-1, -1]]
    if new_number % 3 == 0:
        line = 1
    elif new_number % 3 == 2:
        line = 2
    else:
        line = 3
    column = (new_number - 1) // 3 + 1
    for move in moves:
        ii = move[0]
        jj = move[1]
        if is_corner[line+ii][column+jj]:
            data[roulette]["patterns"]["canto"][line+ii][column+jj] = 0


def update_direta(roulette, new_number):
    data[roulette]["patterns"]["direta"][new_number] = 0


def update_dupla(roulette, new_number):
    if new_number % 3 == 0:
        line = 0
    elif new_number % 3 == 2:
        line = 1
    else:
        line = 2
    column = (new_number - 1) // 3

    if line != 0:
        data[roulette]["patterns"]["dupla"]["down"][line-1][column] = 0
    if line != 2:
        data[roulette]["patterns"]["dupla"]["down"][line][column] = 0

    if column != 0:
        data[roulette]["patterns"]["dupla"]["right"][line][column-1] = 0
    if column != 11:
        data[roulette]["patterns"]["dupla"]["right"][line][column] = 0



def pattern_verification(roulette, new_number):
    for pattern in data[roulette]:
        for num in data[roulette]["patterns"][pattern]:
            num += 1

    update_rua(roulette, new_number)
    update_canto(roulette, new_number)
    update_direta(roulette, new_number)
    uptade_rua_dupla(roulette, new_number)
    update_canto(roulette, new_number)
