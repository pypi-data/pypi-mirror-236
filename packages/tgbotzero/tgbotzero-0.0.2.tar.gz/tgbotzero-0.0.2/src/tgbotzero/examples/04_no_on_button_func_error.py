from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return [
        "Твоё сообщение: " + msg,
        Button('Кнопка есть', 'btn_yes'),
        Button('Кнопки нет', 'btn_lost'),
    ]


def on_button_btn_yes(data):
    return [
        "Кнопка btn_yes",
        Button('Кнопка есть', 'btn_yes'),
        Button('Кнопки нет', 'btn_lost'),
    ]


run_bot()
