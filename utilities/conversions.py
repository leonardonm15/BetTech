def convert_direta_pos_to_num(i, j):
    return j*3 + 1 + (2-i)

def convert_direta_num_to_pos(num):
    if num%3 == 0:
        linha = 0
    elif num%3 == 2:
        linha = 1
    else:
        linha = 2
    coluna = (num-1)//3
    return [linha, coluna]

def convert_canto_pos_to_nums(i, j):
    num = j*3 + 1
    if num%3 == 0:
        num -= 2
    elif num%3 == 1:
        num += 2
    num -= i
    lista = [num, num+3, num-1, num+2]
    return lista

def convert_canto_num_to_pos(num):
    if num%3 == 0:
        linha = 0
    elif num%3 == 2:
        linha = 1
    else:
        linha = 2
    coluna = (num-1)//3
    return [linha, coluna]


def convert_rua_pos_to_nums(i):
    fnum = i*3 + 1
    return [fnum, fnum+1, fnum+2]

def convert_rua_num_to_pos(num):
    return (num-1)//3
