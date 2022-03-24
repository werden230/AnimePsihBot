from telegram import ReplyKeyboardMarkup

DEFAULT_KB = ReplyKeyboardMarkup(
        [
            ["/info", "/roll", "/filter"]
        ], resize_keyboard=True
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
            ["/info", "/roll", "/filter", '/reset']
        ], resize_keyboard=True
)
