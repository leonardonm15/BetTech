def update_last_numbers(table_json_number, bad_input):
    # dado  numeros antigos e 5 novos
    """pega o ultimo numero do velho compara
    com os ultimos dos novos ate achar um igual
    quando achar, pega o de tras do novo e verifica se é o mesmo
    do de tras do velho, dps so corta """

    i = 0
    for json_number in table_json_number[::-1]:
        c = 0
        for number in bad_input[::-1]:
            if number == json_number:
                print(bad_input[-c - 1:-c - 3: -1], table_json_number[-i - 1: -i - 3: -1])
                if bad_input[-c - 1:-c - 4: -1] == table_json_number[-i - 1: -i - 4: -1]: # se o numero de tras for igual tbm ele adiciona os numeros da frente
                    new_numbers = [number for number in bad_input[:-c - 1:-1]]
                    return new_numbers
            c += 1
        i += 1
