import urllib

import requests
from urllib.request import urlopen
import time

global at


def vk_api_handler(id, method):
    if not connect():
        return
    result = list()
    a = requests.get(f'https://api.vk.com/method/{method}?v=5.131&user_id'
                     f'={id}&access_token'
                     f'={at}')
    jsonForParsing = a.json()
    if 'error' in jsonForParsing:
        if 'One of the parameters specified was missing or invalid: album_id ' \
           'is invalid' not in jsonForParsing['error']['error_msg']:
            print("Возникла непредвиденная ситуция. Вероятно, был введен "
                  "неверный токен или доступ к данным пользователя ограничен "
                  "настройками приватности.")
    else:
        print("Начинается обработка запроса")

    match method:
        case 'friends.get':
            print(
                'В целях получения бесперебойной доступности к серверам '
                'Вконтакте включена задержка.\n'
                'Начинается сбор информации о друзьях пользователя.')
            for id in jsonForParsing['response']['items']:
                result.append(get_dataUser(id))

                time.sleep(0.4)
        case 'photos.getAlbums':
            print('В целях получения бесперебойной доступности к серверам '
                  'Вконтакте включена задержка.\n'
                  'Начинается сбор информации об альбомах пользователя.')
            for index in jsonForParsing['response']['items']:
                result.append(index['title'])
                time.sleep(0.5)
        case 'gifts.get':
            print(
                'В целях получения бесперебойной доступности к серверам '
                'Вконтакте включена задержка.\n'
                'Начинается сбор информации о сообщениях у подарков '
                'пользователя.')
            for index in jsonForParsing['response']['items']:

                if index['message']:
                    result.append(index['message'])
                time.sleep(0.5)
        case 'groups.get':
            print(
                'В целях получения бесперебойной доступности к серверам '
                'Вконтакте включена задержка.\n'
                'Начинается сбор информации о группах пользователя.')
            for index in jsonForParsing['response']['items']:
                result.append(get_dataGroup(index))
                time.sleep(0.5)
        case 'wall.get':
            print(
                'В целях получения бесперебойной доступности к серверам '
                'Вконтакте включена задержка.\n'
                'Начинается сбор информации о сообщениях на стене '
                'пользователя.')
            a = requests.get(
                f'https://api.vk.com/method/wall.get?owner_id={id}&v=5.131&&access_token'
                f'={at}')

            for index in a.json()['response']['items']:
                if index['text']:
                    result.append(index['text'])
            time.sleep(0.5)
        case 'photos.get':
            print(
                'В целях получения бесперебойной доступности к серверам '
                'Вконтакте включена задержка.\n'
                'Начинается сбор информации о фотографиях со страницы '
                'пользователя.Фотографии будут загружены в текущую '
                'директорию.')
            a = requests.get(
                f'https://api.vk.com/method/photos.get?owner_id={id}&album_id=profile&&v=5.131&&access_token'
                f'={at}')

            for index in a.json()['response']['items']:
                result.append(index['sizes'][-1]['url'])
                time.sleep(0.5)
            for index, value in enumerate(result):
                urllib.request.urlretrieve(
                    f"{value}",
                    f"0000000{index}.jpg")
                time.sleep(0.5)
        case 'notifications.get' as b:
            print(
                'В целях получения бесперебойной доступности к серверам '
                'Вконтакте включена задержка.\n'
                'Начинается сбор информации об уведомлениях "Мне нравится" у '
                'авторизованного пользователя ')
            a = requests.get(
                f'https://api.vk.com/method/{b}?filters=likes&v=5.131'
                f'&&access_token '
                f'={at}')

            jsonForParsing = a.json()
            for id in jsonForParsing['response']['items']:
                from_ = id['feedback']['items'][0]['from_id']

                result.append(get_dataUser(from_))
                time.sleep(0.5)
    print('Обработка закончена')
    return result


def get_dataUser(id):
    a = requests.get(
        f'https://api.vk.com/method/users.get?v=5.131&user_id'
        f'={id}&access_token'
        f'={at}')

    jsonchin = a.json()

    name = jsonchin['response'][0]['first_name']

    surname = jsonchin['response'][0]['last_name']

    return name + ' ' + surname


def get_dataGroup(id):
    a = requests.get(
        f'https://api.vk.com/method/groups.getById?v=5.131&group_id'
        f'={id}&access_token'
        f'={at}')
    return a.json()['response'][0]['name']

def connect():
    try:
        urlopen('http://google.com')
        return True
    except:
        print("нет соединения")
        return False
if __name__ == '__main__':
    at = input('Введите токен: ')
    id= int(input('Введите id пользователя: '))
    commands = ['photos.get', 'friends.get', 'photos.getAlbums', 'gifts.get',
                'groups.get', 'wall.get', 'notifications.get']
    res = vk_api_handler(id, commands[4])
    if res is not None:
        for i in res:
            print(i)
