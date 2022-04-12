from pymongo import MongoClient
from config import MONGODB_TOKEN


def add_user(user_id, username):
    collection.insert_one({
        '_id': user_id,
        'username': username,
        'filters': {
            'grade': 0,
            'type': None,
            'genre': None
        },
        'total_rolls': 0,
        'last_anime': 351,
        'favs': [],
        'cur_fav_pos': -1
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


def get_parameter(parameter_name, user_id):
    result = collection.find_one({
        '_id': user_id
    })[f'{parameter_name}']
    return result


def set_filter(filter_name, value, user_id):
    collection.update_one({'_id': user_id}, {'$set': {f'filters.{filter_name}': value}})


def set_parameter(parameter_name, value, user_id):
    collection.update_one({'_id': user_id}, {'$set': {f'{parameter_name}': value}})


def set_default_filters(user_id):
    default = {'grade': 0, 'type': None, 'genre': None}
    collection.update_one({'_id': user_id}, {'$set': {'filters': default}})


def update_rolls(user_id):
    collection.update_one({'_id': user_id}, {'$inc': {'total_rolls': 1}})


def add_favourite(anime_id, user_id):
    collection.update_one({'_id': user_id}, {'$push': {'favs': anime_id}})


def delete_favourite(index, user_id):
    anime_id = get_parameter('favs', user_id)[index]
    collection.update_one({'_id': user_id}, {'$pull': {"favs": anime_id}})


def inc_position(user_id):
    collection.update_one({'_id': user_id}, {'$inc': {'cur_fav_pos': 1}})


def dec_position(user_id):
    collection.update_one({'_id': user_id}, {'$inc': {'cur_fav_pos': -1}})


cluster = MongoClient(MONGODB_TOKEN)
db = cluster["AnimePsihBot"]
collection = db["users"]