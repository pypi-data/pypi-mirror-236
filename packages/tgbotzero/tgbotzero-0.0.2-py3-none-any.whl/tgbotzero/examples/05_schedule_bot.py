from tgbotzero import *
import datetime

TOKEN = '123:tokenHereFromBotFatherInTelegram'

times = [
    '09:00 - 09:45',
    '10:00 - 10:45',
    '11:00 - 11:45',
    '12:00 - 12:45',
    '13:00 - 13:45',
    '14:00 - 14:45',
]

monday = [
    'Математика',
    'Литература',
    'История',
    'Биология',
    'Информатика',
    'Физкультура',
]

tuesday = [
    'Английский язык',
    'География',
    'Химия',
    'Литература',
    'Алгебра',
    'Искусство',
]

wednesday = [
    'Физика',
    'Математика',
    'Обществознание',
    'Физкультура',
    'Литература',
    'Английский язык',
]

thursday = [
    'Геометрия',
    'Русский язык',
    'История',
    'Технология',
    'Биология',
    'Музыка',
]

friday = [
    'Алгебра',
    'Английский язык',
    'География',
    'Физика',
    'Искусство',
    'Физкультура',
]

saturday = [
]

sunday = [
]

days_of_week = [
    'понедельник',
    'вторник',
    'среду',
    'четверг',
    'пятницу',
    'субботу',
    'воскресенье',
]
schedule = [monday, tuesday, wednesday, thursday, friday, saturday, saturday, sunday]

buttons = [
    Button('Понедельник', 'btn', 0),
    Button('Вторник', 'btn', 1),
    Button('Среда', 'btn', 2),
    Button('Четверг', 'btn', 3),
    Button('Пятница', 'btn', 4),
]


def on_message(msg: str):
    day_of_week = datetime.datetime.today().weekday()
    return on_button_btn(day_of_week)


def on_button_btn(day_num):
    day = schedule[day_num]
    text = 'Расписание на ' + days_of_week[day_num] + ':\n'
    for les_num in range(len(times)):
        if les_num >= len(day):
            break
        time = times[les_num]
        lesson = day[les_num]
        text += time + ': ' + lesson + '\n'
    return [
        text,
        *buttons,
    ]


run_bot()
