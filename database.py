from pymongo import MongoClient
from config import MONGODB_TOKEN

def add_user(user_id, username):
    collection.insert_one({
        '_id': user_id,
        'username': username,
        'filters': {
            'grade': 0.0,
            'type': '',
            'genre': ''
        },
        'total_rolls': 0,
        'last_anime': 351,
        'favs': []
    })


def get_all_users():
    users = collection.find({})
    bebra = [i['_id'] for i in users]
    return bebra


def get_filter(filter_name, user_id):
    result = collection.find_one({
        '_id': user_id
    })['filters'][f'{filter_name}']
    return result


def get_parametr(parametr_name, user_id):
    result = collection.find_one({
        '_id': user_id
    })[f'{parametr_name}']
    return result


def set_filter(filter_name, value, user_id):
    collection.update_one({'_id': user_id}, {'$set': {f'filters.{filter_name}': value}})


def set_parametr(parametr_name, value, user_id):
    collection.update_one({'_id': user_id}, {'$set': {f'{parametr_name}': value}})


def set_default_filters(user_id):
    default = {'grade': 0.0, 'type': '', 'genre': ''}
    collection.update_one({'_id': user_id}, {'$set': {'filters': default}})


def update_rolls(user_id):
    collection.update_one({'_id': user_id}, {'$inc': {'total_rolls': 1}})


def update_favourites(anime_id, user_id):
    collection.update_one({'_id': user_id}, {'$push': {'favs': anime_id}})


cluster = MongoClient(MONGODB_TOKEN)
db = cluster["AnimePsihBot"]
collection = db["users"]