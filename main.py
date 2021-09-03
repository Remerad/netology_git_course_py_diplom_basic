import json

import requests
from datetime import date
from pprint import pprint
import time
from progress.bar import IncrementalBar
import os

#TODO: запись json файла с параметрами фото

import main

VK_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
photo_list = []
ya_token = ''
photos_owner_id = 'begemot_korovin'


def get_photo_urls_list():
    photos_owner_id = input("Введите id пользователя: ")
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_ids': photos_owner_id,
        'album_id': 'profile',
        'access_token': VK_token,
        'extended': 1,
        'v': '5.77'
    }
    res = requests.get(URL, params=params)
    for photos_data in (res.json()['response']['items']):
        max_size = 0
        max_size_url = ''
        for photo_size in photos_data['sizes']:
            #pprint(photo_size['height'])
            if photo_size['height'] > max_size:
               max_size = photo_size['height']
               max_size_url = photo_size['url']
        #print(max_size, ' - ', max_size_url)
        photo_list.append({'likes': photos_data['likes']['count'],
                           'date': photos_data['date'], 'url': max_size_url}) #date.fromtimestamp(photos_data['date'])
    print(f'Всего фото в профиле: {len(photo_list)}')


def save_photos_from_list():
    likes = []
    name = ''
    for photo in photo_list:
        likes.append(photo['likes'])
    #print(likes)

    bar = IncrementalBar('Сохранение фото:', max=len(photo_list))

    for photo in photo_list:
        if likes.count(photo['likes']) == 1:
            name = str(photo['likes']) + '.jpg'
        else:
            name = str(photo['likes']) + '_' + str(photo['date']) + '.jpg'
        photo.update({'name': name})
        #pprint(photo)

        with open(name, 'wb') as handle:
            response = requests.get(photo['url'], stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

        bar.next()
        with open('photos_data.json', 'w') as handle:
            (json.dump(likes, handle))
    bar.finish()


def upload():
    YA_API_BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    bar = IncrementalBar('Загрузка фото на ЯДиск фото:', max=len(photo_list))
    for photo in photo_list:
        file_path = photo['name']
        headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + ya_token
        }
        params = {
            'path': 'ntl_dipl_folder/' + file_path,
            'overwrite': True
        }
        response = requests.get(YA_API_BASE_URL, params=params, headers=headers)
        #pprint(response.json())
        upload_response = requests.put(url=response.json()['href'], data=open(file_path, 'rb'),
                                       params=params, headers=headers)
        #print(upload_response.status_code)
        bar.next()
    bar.finish()


def folder_maker():
    folder_name = 'ntl_dipl_folder'
    YA_API_BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {
        "Accept": "application/json",
        "Authorization": "OAuth " + ya_token
    }
    params = {
        'path':  '/'+folder_name #
    }
    response = requests.put(YA_API_BASE_URL, params=params, headers=headers)
    pprint(response.json())


if __name__ == '__main__':
    get_photo_urls_list()
    ##pprint(photo_list)
    #save_photos_from_list()
    ##begemot-korovin
    ya_token = input("Введите токен Яндекс-Диска: ")
    print(ya_token)
    folder_maker()
    upload()
    pprint(photo_list)
    os.system('pause')
