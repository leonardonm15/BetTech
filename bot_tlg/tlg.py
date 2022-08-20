import telegram
import dotenv
import os

dotenv.load_dotenv()
token_tlg = os.getenv("TOKEN_TLG")
chat_id = os.getenv("CHAT_ID")
bot = telegram.Bot(token_tlg)


def alerta(padrao, qnt_rodadas, roulette):
    bot.send_message("-738340800", f"ALERTA, O PADRÃO {padrao} NAO OCORRE HÁ {qnt_rodadas} RODADAS NA ROLETA {roulette}")
