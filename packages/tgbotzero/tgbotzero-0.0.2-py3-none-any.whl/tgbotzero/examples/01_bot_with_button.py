from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return [
        "Твоё сообщение: " + msg,
        Button('Кнопка', 'btn'),
    ]


def on_button_btn(data):
    return 'Нажата кнопка. Отправьте любое сообщение для продолжения'


run_bot()
