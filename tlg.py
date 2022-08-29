import telegram
import dotenv
import os
from utilities import conversions

dotenv.load_dotenv()


class BotTlg:
    def __init__(self):
        self.mensagem = '-----------🎲----------- \n'
        self.token_tlg = os.getenv("TOKEN_TLG")
        self.chat_id = os.getenv("CHAT_ID")
        self.bot = telegram.Bot(self.token_tlg)

    def alerta_rua(self, index_rua, qnt_rodadas, roulette, ultimo_numero):
        num1 = index_rua * 3 + 1
        num2 = num1 + 1
        num3 = num2 + 1
        self.mensagem += f"🤖           A RUA DOS NÚMEROS {num1}, {num2} e {num3} NÃO OCORRE HÁ {qnt_rodadas} RODADAS NA ROLETA {roulette}, ULTIMO NÚMERO A SAIR {ultimo_numero}, 11 TENTATIVAS           🤖\n"

    def alerta_rua_dupla(self, index_rua_dupla, rodadas, roulette, ultimo_numero):
        num1 = index_rua_dupla * 3 + 1
        num2 = num1 + 5
        self.mensagem += f"🤖           A RUA DUPLA DOS NÚMEROS {num1} A {num2} NÃO OCORRE HÁ {rodadas} RODADAS NA ROLETA {roulette}, ULTIMO NÚMERO A SAIR {ultimo_numero}, 11 TENTATIVAS           🤖\n"

    def alerta_do_zero(self, menor_num, roulette, ultimo_numero):
        self.mensagem += f"🤖           AGRUPAMENTO DO ZERO (12, 35, 3, 26, 0, 32, 15) NÃO OCORRE HÁ {menor_num} RODADAS NA ROLETA {roulette}, ULTIMO NÚMERO A SAIR {ultimo_numero}, 4 TENTATIVAS           🤖\n"

    def alerta_canto(self, canto_i, canto_j, rodadas, roulette, ultimo_numero):
        nums_array = conversions.convert_canto_pos_to_nums(canto_i, canto_j)
        num1 = nums_array[0]
        num2 = nums_array[1]
        num3 = nums_array[2]
        num4 = nums_array[3]
        self.mensagem += f"🤖           O CANTO DOS NÚMEROS {num1}, {num2}, {num3} E {num4} NÃO OCORRE HÁ {rodadas} RODADAS NA ROLETA {roulette}, ULTIMO NÚMERO A SAIR {ultimo_numero}, 8 TENTATIVAS           🤖\n"

    def alerta_direta(self, num, rodadas, roulette, ultimo_numero):
        self.mensagem += f"🤖           O NÚMERO {num} NÃO OCORRE HÁ {rodadas} RODADAS NA ROLETA {roulette}, ULTIMO NÚMERO A SAIR {ultimo_numero}, 30 TENTATIVAS           🤖\n"

    def alerta_dupla(self, dupla_i, dupla_j, direction, rodadas, roulette, ultimo_numero):
        num1 = conversions.convert_direta_pos_to_num(dupla_i, dupla_j)
        if direction == "right":
            num2 = num1 + 3
        else:
            num2 = num1 + 1
        self.mensagem += f"🤖           A DUPLA DOS NÚMEROS {num1} E {num2} NÃO OCORRE HÁ {rodadas} RODADAS NA ROLETA {roulette}, ULTIMO NÚMERO A SAIR {ultimo_numero}, 17 TENTATIVAS           🤖\n"

    def send_message(self):
        if self.mensagem == "-----------🎲----------- \n":
            print("mensagem vazia, nada de importante aconteceu")
            return

        self.mensagem += '-----------🎲-----------'
        if len(self.mensagem) > 4096:
            self.bot.send_message(self.chat_id, self.mensagem[:4096])
            self.bot.send_message(self.chat_id, self.mensagem[4096:])
            self.mensagem = '-----------🎲-----------\n'
            return
        self.bot.send_message(self.chat_id, self.mensagem)
        self.mensagem = '-----------🎲----------- \n'
        return
