from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return [
        "Твоё сообщение: " + msg,
        Button('Кнопка', 'btn1', 1),
        Button('Кнопка', 'btn1', 2),
        Button('Кнопка 3', 'btn3'),
    ]


def on_button_btn1(data):
    if data == 1:
        text = 'Первая кнопка'
    else:
        text = 'Вторая кнопка'
    return [
        text,
        Button('Кнопка 3', 'btn3'),
    ]


def on_button_btn3(data):
    return 'Это — уникальная третья кнопка. Отправьте любое сообщение для продолжения'


run_bot()
