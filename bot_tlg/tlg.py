import telegram
import dotenv
import os

dotenv.load_dotenv()

token_tlg = os.getenv("TOKEN_TLG")
chat_id = os.getenv("CHAT_ID")

bot = telegram.Bot(token_tlg)


def alerta(padrao, qnt_rodadas, numero_mesa):
    bot.send_message("-738340800", f"ALERTA, O PADRÃO {padrao} NAO OCORRE A {qnt_rodadas} RODADAS NA MESA {numero_mesa}")
