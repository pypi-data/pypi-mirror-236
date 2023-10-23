from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return "Твоё сообщение: " + msg
