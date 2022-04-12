from datetime import datetime
import locale


locale.setlocale(locale.LC_TIME, "ru_RU")

START_MESSAGE = """Привет! Этот бот может скинуть тебе случайное аниме с сайта Шикимори.
Начать поиск - /roll
Настроить фильтр - /filter
Список избранного - /favs
Приятного пользования!"""

ANIME_TYPES = {'ona': 'ona',
               'ova': 'ova',
               'tv сериал': 'tv',
               'фильм': 'movie',
               None: None}

ANIME_GENRES = {'сёнен': 27, 'сёнен-ай': 28, 'сэйнэн': 42, 'сёдзё': 25, 'сёдзё-ай': 26, 'дзёсей': 43, 'комедия': 4,
                'романтика': 22, 'школа': 23, 'безумие': 5, 'боевые искусства': 17, 'вампиры': 32, 'военное': 38,
                'гарем': 35, 'гурман': 543, 'демоны': 6, 'детектив': 7, 'детское': 15, 'драма': 8, 'игры': 11,
                'исторический': 13, 'космос': 29, 'магия': 16, 'машины': 3, 'меха': 18, 'музыка': 19, 'пародия': 20,
                'повседневность': 36, 'полиция': 39, 'приключения': 2, 'психологическое': 40, 'работа': 541,
                'самураи': 21, 'сверхъестественное': 37, 'спорт': 30, 'супер сила': 31, 'ужасы': 14, 'фантастика': 24,
                'фэнтези': 10, 'экшен': 1, 'этти': 9, 'триллер': 41, 'эротика': 539, 'хентай': 12, 'яой': 33, 'юри': 34,
                None: None}


FORMAT = {'tv': "TV Сериал",
          'movie': "Фильм",
          'ona': "ONA",
          'ova': "OVA",
          'released': "вышло",
          'ongoing': "онгоинг",
          'anons': "анонсировано",
          'g': 'G',
          'pg': 'PG',
          'pg_13': 'PG-13',
          'r': 'R',
          'r_plus': 'R+',
          'rx': 'Rx',
          None: '-'
          }


def get_duration(mins):
    m = mins % 60
    h = mins // 60
    format_rule = {
        h == 0: "{m} мин.",
        h == 1: "1 час {m} мин.",
        h > 1: "{h} часа {m} мин.",
        h == 1 and m == 0: "1 час",
        h > 1 and m == 0: "{h} часа"
    }
    duration = [format_rule[condition].format(m=m, h=h) for condition in format_rule if condition][0]
    return duration


def get_status(a_status, start, stop):
    start = datetime.strptime(start, '%Y-%m-%d')
    stop = datetime.strptime(stop, '%Y-%m-%d') if stop else None
    if a_status == "вышло" and stop:
        status = f'вышло в {start.strftime("%Y")}-{stop.strftime("%Y")} гг.'
    elif a_status == "вышло" and not stop:
        status = f'вышло {start.strftime("%d %b %Y").strip("0")} г.'
    elif a_status == "онгоинг":
        status = f'онгоинг с {start.strftime("%d %b %Y").strip("0")} г.'
    else:
        status = '-'
    return status


def get_episodes(status, episodes, episodes_aired):
    if status == 'released':
        return episodes
    elif status == 'ongoing':
        episodes = "?" if episodes == 0 else episodes
        return f'{episodes_aired} / {episodes}'
    else:
        return "?"


def create_message(anime: dict):
    message = f'*{anime["name"]}*' \
              f'\nТип: {FORMAT[anime["kind"]]}' \
              f'\nОценка: {anime["score"]}' \
              f'\nЭпизоды: {get_episodes(anime["status"], anime["episodes"], anime["episodes_aired"])}' \
              f'\nДлительность эпизода: {get_duration(anime["duration"])}' \
              f'\nСтатус: {get_status(FORMAT[anime["status"]], anime["aired_on"], anime["released_on"])}' \
              f'\nРейтинг: {FORMAT[anime["rating"]]}' \
              f'\nОписание: {anime["description"]}' \
              f'\nЖанры: {", ".join(anime["genres"])}'
    if len(message) > 1024:
        desc = anime['description']
        desc = desc[:1024 - len(message) - len("читать дальше...")]
        desc = '.'.join(desc.split('.')[:-1]) + f'. [Читать дальше...]({anime["link"]})'
        message = message.split("\n")
        message[7] = f'Описание: {desc}'
        message = '\n'.join(message)
    return message