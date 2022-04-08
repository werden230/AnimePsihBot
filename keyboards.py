from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton


PREV = 'callback_prev'
DEL = 'callback_del'
NEXT = 'callback_next'


TITLES = {PREV: '\u2B05',
          DEL: '\u274C',
          NEXT: '\u27A1'}


def get_first_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[NEXT], callback_data=NEXT)
        ],
        [
            InlineKeyboardButton(TITLES[DEL], callback_data=DEL)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[PREV], callback_data=PREV),
            InlineKeyboardButton(TITLES[NEXT], callback_data=NEXT)
        ],
        [
            InlineKeyboardButton(TITLES[DEL], callback_data=DEL)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_last_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[PREV], callback_data=PREV)
        ],
        [
            InlineKeyboardButton(TITLES[DEL], callback_data=DEL)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_single_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[DEL], callback_data=DEL)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


INLINE_KBS = {'last': get_last_keyboard(),
              'first': get_first_keyboard(),
              'middle': get_main_keyboard(),
              'single': get_single_keyboard()}


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

DEFAULT_KB = ReplyKeyboardMarkup(
        [
            ["/favs", "/roll", "/filter"],
            ["❤"]
        ], resize_keyboard=True
)
