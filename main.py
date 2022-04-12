import logging
import strings
import database as db
import keyboards as kb
import scraping as scr
from telegram import Update
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.files.inputmedia import InputMediaPhoto
from config import TG_TOKEN


# /start command
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in db.get_all_users():
        username = update.effective_user.username
        db.add_user(user_id, username)
    update.message.reply_text(text=strings.START_MESSAGE, reply_markup=kb.DEFAULT_KB)


def roll(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        score = db.get_filter('grade', user_id)
        kind = db.get_filter('type', user_id)
        genre = db.get_filter('genre', user_id)
        anime = scr.get_random_anime(score=score, kind=kind, genre=genre)
        message = strings.create_message(anime)
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Подробнее на Шики", url=anime["link"])]
            ]
        )
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=anime["img"],
            caption=message,
            parse_mode='MARKDOWN',
            reply_markup=reply_markup
        )
        db.set_parameter('last_anime', anime['id'], update.effective_user.id)
    except IndexError:
        update.message.reply_text(text="Такого аниме не нашлось...")
    except:
        update.message.reply_text(text="Чёто случилось, я сам не пойму чё. Ещё раз попробуй, только нормально.")
    else:
        db.update_rolls(update.effective_user.id)


def add_to_fav(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    anime_id = db.get_parameter('last_anime', user_id)
    if anime_id in db.get_parameter('favs', user_id):
        update.message.reply_text("Аниме уже есть в избранном!")
        return
    db.add_favourite(anime_id, user_id)
    update.message.reply_text("Аниме добавлено в избранное!")


def get_favs(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    favs = db.get_parameter('favs', user_id)
    if len(favs) == 0:
        context.bot.send_message(chat_id=chat_id, text='Список избранного пуст!')
        return
    db.set_parameter('cur_fav_pos', 0, user_id)
    anime_id = favs[0]
    anime = scr.get_anime(anime_id)
    message = strings.create_message(anime)
    context.bot.send_photo(
        chat_id=chat_id,
        photo=anime["img"],
        caption=message+f"\n\n1/{len(favs)}",
        parse_mode='MARKDOWN',
        reply_markup=kb.get_first_keyboard() if len(favs) > 1 else kb.get_single_keyboard()
    )


def check_status(index: int, favs: list):
    if len(favs) == 1:
        status = 'single'
    elif index == 0:
        status = 'first'
    elif index == len(favs)-1:
        status = 'last'
    else:
        status = 'middle'
    return status


def favs_keyboard_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if data in (kb.NEXT, kb.PREV):
        favs = db.get_parameter('favs', user_id)
        db.inc_position(user_id) if data == kb.NEXT else db.dec_position(user_id)
        index = db.get_parameter('cur_fav_pos', user_id)
        anime_id = favs[index]
        anime = scr.get_anime(anime_id)
        message = strings.create_message(anime)
        status = check_status(index, favs)
        query.message.edit_media(
            InputMediaPhoto(
                media=anime["img"],
                caption=message+f"\n\n{index+1}/{len(favs)}",
                parse_mode='MARKDOWN'
            ),
            reply_markup=kb.INLINE_KBS[status]
        )
    elif data == kb.DEL:
        index = db.get_parameter('cur_fav_pos', user_id)
        db.delete_favourite(index, user_id)
        favs = db.get_parameter('favs', user_id)
        if favs:
            if index < len(favs):
                anime_id = favs[index]
            else:
                anime_id = favs[index - 1]
                db.dec_position(user_id)
                index -= 1
            anime = scr.get_anime(anime_id)
            status = check_status(index, favs)
            message = strings.create_message(anime)
            query.message.edit_media(
                InputMediaPhoto(
                    media=anime["img"],
                    caption=message+f"\n\n{index+1}/{len(favs)}",
                    parse_mode='MARKDOWN'
                ),
                reply_markup=kb.INLINE_KBS[status]
            )
        else:
            query.delete_message()
            context.bot.send_message(chat_id=chat_id, text='Список избранного пуст!')


# /filter command
def start_filter(update: Update, context: CallbackContext):
    update.message.reply_text(text="Выбери оценку, ниже которой аниме не будет выбираться.", reply_markup=kb.GRADES_KB)
    return 1


def pick_grade(update: Update, context: CallbackContext):
    try:
        answer = update.message.text
        grade = 6 if answer == "Неважно" else max(int(answer), 6)
        db.set_filter('grade', grade, update.effective_user.id)
    except ValueError:
        update.message.reply_text(text="Введи оценку правильно!")
        return 1
    update.message.reply_text(text="Выбери желаемый тип аниме.", reply_markup=kb.TYPES_KB)
    return 2


def pick_type(update: Update, context: CallbackContext):
    answer = update.message.text.lower()
    type = None if answer == 'неважно' else answer
    if type and type not in strings.ANIME_TYPES:
        update.message.reply_text(text="Такого типа не существует, попробуй ещё раз =)")
        return 2
    db.set_filter('type', strings.ANIME_TYPES[type], update.effective_user.id)
    update.message.reply_text(text="Выбери желаемый жанр аниме.", reply_markup=kb.GENRES_KB)
    return 3


def pick_genre(update: Update, context: CallbackContext):
    answer = update.message.text.lower()
    genre = None if answer == 'неважно' else answer
    if genre and genre not in strings.ANIME_GENRES:
        update.message.reply_text(text="Такого жанра не существует, попробуй ещё раз =)")
        return 3
    db.set_filter('genre', strings.ANIME_GENRES[genre], update.effective_user.id)
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
    update.message.reply_text(text=f"Общее количество роллов: {db.get_parameter('total_rolls', user_id)}\n"
                                   f"Количество аниме в избранном: {len(db.get_parameter('favs', user_id))}")


def main():
    updater = Updater(
        token=TG_TOKEN
    )
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    roll_handler = CommandHandler('roll', roll)
    add_fav_handler = MessageHandler(Filters.text('❤'), add_to_fav)
    get_favs_handler = CommandHandler('favs', get_favs)
    favs_buttons_handler = CallbackQueryHandler(callback=favs_keyboard_handler)
    statistic_handler = CommandHandler('stat', statistic)
    default_handler = CommandHandler('reset', reset)
    sorting_handler = ConversationHandler(
        entry_points=[CommandHandler('filter', start_filter)],
        states={
            1: [MessageHandler(Filters.text & (~Filters.command), pick_grade)],
            2: [MessageHandler(Filters.text & (~Filters.command), pick_type)],
            3: [MessageHandler(Filters.text & (~Filters.command), pick_genre)]
        },
        fallbacks=[CommandHandler('cancel', cancel)])

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_fav_handler)
    dispatcher.add_handler(get_favs_handler)
    dispatcher.add_handler(favs_buttons_handler)
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
