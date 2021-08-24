import requests
from datetime import date
from pprint import pprint

token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
photo_list = []

def get_photo_urls_list():
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_ids': 'begemot_korovin',
        'album_id': 'profile',
        'access_token': token,
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

def prepare_photos_hames():
    for photo in photo_list:
        print(photo['likes'])


def save_photos_from_list():
    likes = []
    name = ''
    for photo in photo_list:
        if photo['likes'] not in likes:
            name = str(photo['likes'])
            likes.append(photo['likes'])
        else:
            name = str(photo['likes'] + photo['date'])

        with open(name + '.jpg', 'wb') as handle:
            response = requests.get(photo['url'], stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)


if __name__ == '__main__':
    get_photo_urls_list()
    pprint(photo_list)
    prepare_photos_hames()