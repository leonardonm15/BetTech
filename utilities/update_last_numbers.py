def update_last_numbers(old_table, new_table):
    # dado  numeros antigos e 5 novos
    """pega o ultimo numero do velho compara
    com os ultimos dos novos ate achar um igual
    quando achar, pega o de tras do novo e verifica se é o mesmo
    do de tras do velho, dps so corta """

    #i = 0
    # for json_number in table_json_number[::-1]:
    #     c = 0
    #     for number in bad_input[::-1]:
    #         if number == json_number:
    #             print(bad_input[-c - 1:-c - 3: -1], table_json_number[-i - 1: -i - 3: -1])
    #             if bad_input[-c - 1:-c - 4: -1] == table_json_number[-i - 1: -i - 4: -1]: # se o numero de tras for igual tbm ele adiciona os numeros da frente
    #                 new_numbers = [number for number in bad_input[:-c - 1:-1]]
    #                 if new_numbers is []:
    #                     new_numbers = None
    #                 return new_numbers
    #         c += 1
    #     i += 1

    """ quando acha um elemento igual entre lista velha e lista nova, verifica se
    aquele é realmente o ponto em que a lista velha começa a "aparecer" na lista nova, 
    se for termina, se não continua. Esse teste consiste em ir até o final da lista nova e
    verificar se todos os outros elementos coincidem com a lista velha. Algoritmo roda em O(n) average, sendo 
    n o tamanaho das listas. Também trata o caso em que o programa está iniciando e não há 
    lista velha para comparar """

    new_numbers = []
    json_num_pointer = 0
    num_pointer = 0
    beginning_of_old = -1
    while json_num_pointer < len(old_table) and num_pointer < len(new_table):
        if old_table[json_num_pointer] == new_table[num_pointer]:
            temp_num_pointer = num_pointer + 1
            temp_json_num_pointer = json_num_pointer + 1
            is_beginning_of_old = True
            while temp_num_pointer < len(new_table):
                if old_table[temp_json_num_pointer] != new_table[temp_num_pointer]:
                    is_beginning_of_old = False
                temp_num_pointer += 1
                temp_json_num_pointer += 1
            if is_beginning_of_old:
                beginning_of_old = num_pointer
                break
        num_pointer += 1

    if beginning_of_old < 0:
        # nao achou lista velha na lista nova, provavelmente o programa está iniciando agora
        new_numbers = new_table
    else:
        for i in range(beginning_of_old):
            new_numbers.append(new_table[i])
    return new_numbers
