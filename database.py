import sqlite3 as sq


def init_db():
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER NOT NULL PRIMARY KEY,
                username TEXT,
                grade REAL DEFAULT 0,
                type TEXT DEFAULT '',
                genre TEXT DEFAULT '',
                total_rolls INTEGER DEFAULT 0)""")
    con.close()


def add_user(user_id, username):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO users (user_id, username) VALUES ('{user_id}', '{username}')")
    con.close()


def get_all_users():
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users")
        result = [i[0] for i in cur.fetchall()]
    con.close()
    return result


def get_parametr(parametr, user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT {parametr} FROM users WHERE user_id == {user_id}")
        result = cur.fetchone()[0]
    con.close()
    return result


def set_parametr(parametr_name, parametr, user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"UPDATE users SET {parametr_name} = '{parametr}' WHERE user_id == {user_id}")
    con.close()


def set_default_filters(user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"UPDATE users SET grade = 0, type = '', genre = '' WHERE user_id == {user_id}")
    con.close()


def update_rolls(user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"UPDATE users SET total_rolls = total_rolls+1 WHERE user_id == {user_id}")
    con.close()


def update_favourites(anime_id, user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"UPDATE users SET favs = '{get_parametr('favs', user_id) + anime_id}' WHERE user_id == {user_id}")
    con.close()