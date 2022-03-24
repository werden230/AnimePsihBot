import logging
import json
import strings
import database as db
import keyboards as kb
from random import choice
from telegram import Update
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from config import TG_TOKEN


# /start command
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in db.get_all_users():
        username = update.effective_user.username
        db.add_user(user_id, username)
    update.message.reply_text(text=strings.START_MESSAGE, reply_markup=kb.DEFAULT_KB)


# /info command
def info(update: Update, context: CallbackContext):
    update.message.reply_text(text=strings.INFO_MESSAGE)


# filter by anime rating
def filter_grade(animes: list, grade: float):
    if not grade or grade == "неважно":
        return animes
    return list(filter(lambda x: grade <= float(x["Оценка на MAL"]), animes))


# filter by anime type
def filter_type(animes: list, kind: str):
    if not kind or kind == "неважно":
        return animes
    return list(filter(lambda x: kind.lower() == x["Тип"].lower(), animes))


# filter by anime genre
def filter_genre(animes: list, genre: str):
    if not genre or genre == "неважно":
        return animes
    return list(filter(lambda x: genre.lower() in x["Жанры"].lower(), animes))


def create_message(anime: dict):
    length = sum([len(x + y) for x, y in anime.items()]) - len(anime['link']) - len(anime['image'])
    if length > 1024:
        desc = anime['Описание']
        desc = desc[:1024 - length - len("читать дальше...")]
        desc = '.'.join(desc.split('.')[:-1]) + f'. [Читать дальше...]({anime["link"]})'
        anime['Описание'] = desc
    message = f'*{anime["Название"]}*' \
              f'\nТип: {anime["Тип"]}' \
              f'\nОценка: {anime["Оценка на MAL"]}' \
              f'\nЭпизоды: {anime["Эпизоды"]}' \
              f'\nДлительность эпизода: {anime["Длительность эпизода"]}' \
              f'\nСтатус: {anime["Статус"]}' \
              f'\nРейтинг: {anime["Рейтинг"]}' \
              f'\nОписание: {anime["Описание"]}' \
              f'\nЖанры: {anime["Жанры"]}'
    return message


def get_anime(user_id):
    with open('sorted.json', 'r', encoding='utf-8') as file:
        t = file.read()
        animes = json.loads(t)
        animes = filter_grade(animes, db.get_grade(user_id))
        animes = filter_type(animes, db.get_type(user_id))
        animes = filter_genre(animes, db.get_genre(user_id))
        anime = choice(animes)
    return anime


def roll(update: Update, context: CallbackContext):
    try:
        anime = get_anime(update.effective_user.id)
        message = create_message(anime)
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Подробнее на Шики", url=anime["link"])]
            ]
        )
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=anime["image"],
            caption=message,
            parse_mode='MARKDOWN',
            reply_markup=reply_markup
        )
    except IndexError:
        update.message.reply_text(text="Такого аниме не нашлось...")
    except:
        update.message.reply_text(text="Чёто случилось, я сам не пойму чё. Ещё раз попробуй, только нормально.")
    else:
        db.update_rolls(update.effective_user.id)


# /filter command
def start_filter(update: Update, context: CallbackContext):
    update.message.reply_text(text="Выбери оценку, ниже которой аниме не будет выбираться.", reply_markup=kb.GRADES_KB)
    return 1


def pick_grade(update: Update, context: CallbackContext):
    try:
        answer = update.message.text
        grade = 0 if answer == "Неважно" else float(answer)
        db.set_anime_grade(update.effective_user.id, grade)
    except ValueError:
        update.message.reply_text(text="Введи оценку правильно!")
        return 1
    update.message.reply_text(text="Выбери желаемый тип аниме.", reply_markup=kb.TYPES_KB)
    return 2


def pick_type(update: Update, context: CallbackContext):
    answer = update.message.text.lower()
    type = '' if answer == 'неважно' else answer
    if type and type not in strings.ANIME_TYPES_SIMPLIFIED:
        update.message.reply_text(text="Такого типа не существует, попробуй ещё раз =)")
        return 2
    db.set_anime_type(update.effective_user.id, type)
    update.message.reply_text(text="Выбери желаемый жанр аниме.", reply_markup=kb.GENRES_KB)
    return 3


def pick_genre(update: Update, context: CallbackContext):
    answer = update.message.text.lower()
    genre = '' if answer == 'неважно' else answer
    if genre and genre not in strings.ANIME_GENRES:
        update.message.reply_text(text="Такого жанра не существует, попробуй ещё раз =)")
        return 3
    db.set_anime_genre(update.effective_user.id, genre)
    update.message.reply_text(text="Фильтр успешно настроен!", reply_markup=kb.RESET_KB)
    return ConversationHandler.END


# /reset command
def reset(update: Update, context: CallbackContext):
    db.set_default_filters(update.effective_user.id)
    update.message.reply_text(text="Фильтры сброшены!", reply_markup=kb.DEFAULT_KB)


# /cancel command
def cancel(update: Update, context: CallbackContext):
    db.set_default_filters(update.effective_user.id)
    update.message.reply_text(text="Настройка фильтра отменена", reply_markup=kb.DEFAULT_KB)
    return ConversationHandler.END


def statistic(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text(text=f"Общее количество роллов: {db.get_rolls(user_id)}")


def main():
    updater = Updater(
        token=TG_TOKEN
    )
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    roll_handler = CommandHandler('roll', roll)
    statistic_handler = CommandHandler('stat', statistic)
    default_handler = CommandHandler('reset', reset)
    sorting_handler = ConversationHandler(
        entry_points=[CommandHandler('filter', start_filter)],
        states={
            1: [MessageHandler(Filters.text & (~Filters.command), pick_grade)],
            2: [MessageHandler(Filters.text & (~Filters.command), pick_type)],
            3: [MessageHandler(Filters.text & (~Filters.command), pick_genre)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(roll_handler)
    dispatcher.add_handler(statistic_handler)
    dispatcher.add_handler(default_handler)
    dispatcher.add_handler(sorting_handler)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    updater.start_polling()


if __name__ == "__main__":
    main()
