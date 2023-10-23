import os
import sys
import atexit
import traceback
import types
import json
from typing import Union, Tuple, Optional

import telebot
import telebot.types

from tgbotzero.utils.help import help
from tgbotzero.utils.reply_markup import Button, response_to_text_and_buttons
from tgbotzero.utils.check_on_button_functions import check_on_button_functions

bot = telebot.TeleBot('123:tokenHereFromBotFatherInTelegram')
already_started = False
main_module: Optional[types.ModuleType] = None


def handle_all_messages(message: telebot.types.Message):
    bot.send_message(message.chat.id, "BotZero работает только с текстовыми сообщениями.")


def set_up_token(bot: telebot.TeleBot, main_module: types.ModuleType):
    token = getattr(main_module, "TOKEN", None)
    if not token or 'BotFather' in token:
        token = os.environ.get('TOKEN', None)
    if not token:
        help()
        raise ValueError('Необходимо в переменную TOKEN записать токен телеграм-бота. Как-то так: '
                         'TOKEN = "123123123:abcabcabcabcabcabcabcabcabc"')
    bot.token = token


def set_up_on_text_message(bot: telebot.TeleBot, main_module: types.ModuleType):
    on_message = getattr(main_module, "on_message", None)
    if not on_message:
        help()
        raise ValueError('Необходимо определить функцию on_message. Например, так:'
                         'def on_message(msg: str):'
                         '    return "Твоё сообщение: " + msg')

    def on_text_message(message: telebot.types.Message):
        try:
            answer = on_message(message.text)
        except Exception as e:
            bot.send_message(message.from_user.id, f'Возникла ошибка:\n{traceback.format_exc()}')
            raise
        text, reply_markup = response_to_text_and_buttons(answer)
        bot.send_message(message.from_user.id, text, reply_markup=reply_markup)

    bot.message_handler(content_types=['text'])(on_text_message)


def set_up_default_handler(bot: telebot.TeleBot, main_module: types.ModuleType):
    bot.message_handler(func=lambda message: True)(handle_all_messages)


def print_bot_info(bot: telebot.TeleBot):
    bot_info = bot.get_me()
    bot_name = bot_info.username

    print('Бот ждёт: https://t.me/' + bot_name)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(callback_obj: telebot.types.CallbackQuery):
    name, data = callback_obj.data.split(";", maxsplit=1)
    data = json.loads(data)
    callback_function_name = f'on_button_{name}'
    callback_function = getattr(main_module, callback_function_name, None)
    raise_exc = None
    if not callback_function:
        answer = (f"Необходимо определить функцию {callback_function_name}. Например:\n"
                  f"def {callback_function_name}(data):\n"
                  f"    return 'Нажата кнопка {name}, данные: ' + repr(data)\n")
        raise_exc = ValueError(answer)
    else:
        try:
            answer = callback_function(data)
        except Exception as e:
            answer = f'Возникла ошибка:\n{traceback.format_exc()}'
            raise_exc = e

    bot.edit_message_reply_markup(chat_id=callback_obj.message.chat.id,
                                  message_id=callback_obj.message.message_id,
                                  reply_markup=None)
    text, reply_markup = response_to_text_and_buttons(answer)
    bot.send_message(callback_obj.from_user.id, text, reply_markup=reply_markup)
    bot.answer_callback_query(callback_query_id=callback_obj.id)
    if raise_exc:
        raise raise_exc


def run_bot():
    global already_started
    if already_started:
        return
    already_started = True

    global main_module
    main_module = sys.modules["__main__"]

    set_up_token(bot, main_module)
    set_up_on_text_message(bot, main_module)
    set_up_default_handler(bot, main_module)
    check_on_button_functions(main_module)

    # Now we start polling
    print_bot_info(bot)
    bot.infinity_polling()


if __name__ == '__main__':
    print('Модуль должен быть импортирован:\nfrom tgbotzero import *')
    sys.exit()

atexit.register(run_bot)
