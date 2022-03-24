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


def get_grade(user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT grade FROM users WHERE user_id == {user_id}")
        result = cur.fetchone()[0]
    con.close()
    return result


def get_type(user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT type FROM users WHERE user_id == {user_id}")
        result = cur.fetchone()[0]
    con.close()
    return result


def get_genre(user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT genre FROM users WHERE user_id == {user_id}")
        result = cur.fetchone()[0]
    con.close()
    return result


def set_anime_grade(user_id, grade):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"UPDATE users SET grade = {grade} WHERE user_id == {user_id}")
    con.close()


def set_anime_type(user_id, type):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"UPDATE users SET type = '{type}' WHERE user_id == {user_id}")
    con.close()


def set_anime_genre(user_id, genre):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"UPDATE users SET genre = '{genre}' WHERE user_id == {user_id}")
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


def get_rolls(user_id):
    with sq.connect('users_data.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT total_rolls FROM users WHERE user_id == {user_id}")
        result = cur.fetchone()[0]
    con.close()
    return result
