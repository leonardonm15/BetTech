
def update_rua(roulette, new_number, data):
    index = (new_number-1)//3
    data[roulette]["patterns"]["rua"][index] = 0


def uptade_rua_dupla(roulette, new_number, data):
    index = (new_number-1)//3
    if index > 0:
        data[roulette]["patterns"]["rua_dupla"][index-1] = 0

    if index < 10:
        data[roulette]["patterns"]["rua_dupla"][index+1] = 0


def update_canto(roulette, new_number, data):
    is_corner = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    moves = [[0, 0], [0, -1], [-1, 0], [-1, -1]]
    if new_number % 3 == 0:
        line = 0
    elif new_number % 3 == 2:
        line = 1
    else:
        line = 2
    column = (new_number - 1) // 3
    for move in moves:
        ii = move[0]
        jj = move[1]
        if line + ii < 0 or line + jj < 0:
            continue
        if is_corner[line+ii][column+jj]:
            data[roulette]["patterns"]["canto"][line+ii][column+jj] = 0


def update_direta(roulette, new_number, data):
    data[roulette]["patterns"]["direta"][new_number] = 0


def update_dupla(roulette, new_number, data):
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


def pattern_verification(roulette, new_number, data):

    update_rua(roulette, new_number, data)
    update_canto(roulette, new_number, data)
    update_direta(roulette, new_number, data)
    uptade_rua_dupla(roulette, new_number, data)
    update_canto(roulette, new_number, data)
