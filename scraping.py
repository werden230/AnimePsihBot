import requests
from bs4 import BeautifulSoup


def get_anime(anime_id):
    headers = {'user-agent': 'AnimePsihBot'}
    url = f'https://shikimori.one/api/animes/{anime_id}'
    res = requests.get(url=url, headers=headers).json()
    anime = {'id': res['id'],
             'name': res['russian'],
             'kind': res['kind'],
             'score': res['score'],
             'episodes': res['episodes'],
             'episodes_aired': res['episodes_aired'],
             'duration': res['duration'],
             'status': res['status'],
             'aired_on': res['aired_on'],
             'released_on': res['released_on'],
             'rating': res['rating'],
             'description': BeautifulSoup(res['description_html'], "lxml").text,
             'genres': [genre['russian'] for genre in res['genres']],
             'link': "https://shikimori.one" + res['url'],
             'img': "https://shikimori.one" + res['image']['original']
             }
    return anime


def get_random_anime(**kwargs):
    headers = {'user-agent': 'AnimePsihBot'}
    url = 'https://shikimori.one/api/animes'
    params = {key: value for (key, value) in kwargs.items()}
    params['order'] = 'random'
    params['score'] = 6 if not params.get('score') else params['score']
    params['kind'] = ['!music', '!special'] if not params.get('kind') else params['kind']
    res = requests.get(url=url, params=params, headers=headers).json()[0]
    return get_anime(res['id'])