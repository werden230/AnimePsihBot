from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

DEFAULT_KB = ReplyKeyboardMarkup(
        [
            ["/favs", "/roll", "/filter"],
            ["❤"]
        ], resize_keyboard=True
)

PREV = 'callback_prev'
DEL = 'callback_del'
NEXT = 'callback_next'


TITLES = {PREV: '\u2B05',
          DEL: '\u27A1',
          NEXT: '\u27A1'}


FIRST_FAV = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(TITLES[NEXT], callback_data=NEXT)]
    ]
)

FAV = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(TITLES[PREV], callback_data=PREV),
         InlineKeyboardButton(TITLES[NEXT], callback_data=NEXT)]
    ]
)

LAST_FAV = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(TITLES[PREV], callback_data=PREV)]
    ]
)

GRADES_KB = ReplyKeyboardMarkup(
        [
            ["7", "8", "9"],
            ["Неважно", "/cancel"]
        ], resize_keyboard=True
)

TYPES_KB = ReplyKeyboardMarkup(
    [
        ["TV Сериал", "Фильм", "OVA", "ONA"],
        ["Неважно", "/cancel"]
    ], resize_keyboard=True
)

GENRES_KB = ReplyKeyboardMarkup(
        [
            ["Романтика", "Повседневность", "Спорт"],
            ['Фэнтези', "Меха", "Экшен"],
            ["Неважно", "/cancel"]
        ], resize_keyboard=True
)

RESET_KB = ReplyKeyboardMarkup(
        [
            ["/favs", "/roll", "/filter", '/reset'],
            ["❤"]
        ], resize_keyboard=True
)
