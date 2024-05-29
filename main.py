import requests
import datetime
import json
from tqdm import tqdm as progressbar
import os
from dotenv import load_dotenv
from dotenv import dotenv_values


class VK:

    def __init__(self, access_token_init, user_id_init, version='5.131'):

        self.photo_json = {'items': []}
        self.token = access_token_init
        self.id = user_id_init
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    # Getting user information from vk
    def users_info(self):

        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    # Retrieving a photo from vk
    def users_photo(self, count_photo=5):

        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1, 'count': count_photo}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    # Creates a folder for photos
    @staticmethod
    def create_backup_folder(token):

        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        params = {'path': 'Backup_Photo_BK'}
        response = requests.put(url, params={**params}, headers=headers)
        return response.json()

    # The function uploads a photo, creates a dictionary for the 'json-file' and tracks the progress of the upload.
    def keep_photo(self, photos_info, token):

        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}

        bank_likes = set()
        bar = progressbar(total=len(photos_info['response']['items']), desc="Loading…", ascii=False, ncols=100)

        for item in photos_info['response']['items']:

            # Checking for the same number of likes
            if item['likes']['count'] in bank_likes:
                date = datetime.datetime.fromtimestamp(int(item['date']))
                photo_name = f'{item['likes']['count']}({date.date()}).jpg'
            else:
                photo_name = f'{item['likes']['count']}.jpg'
                bank_likes.add(item['likes']['count'])

            # Gets the tuple of the form: (url, size_type)
            params_photo = self.__best_size(item['sizes'])

            # Publishing a picture on Yandex disk
            params = {'path': f'Backup_Photo_BK/{photo_name}', 'url': params_photo[0]}
            requests.post(url, params={**params}, headers=headers)

            # Added file name and size in dictionary
            self.photo_json['items'].append({'file_name': photo_name, 'size': params_photo[1]})

            # Progress bar update
            bar.update(1)

    # Search for photos with maximum resolution
    @staticmethod
    def __best_size(sizes):

        url = ''
        size_types = ['s', 'm', 'x', 'o', 'p', 'q', 'r', 'y', 'z', 'w']
        max_size = 0

        for item in sizes:
            if item['type'] in size_types:
                if size_types.index(item['type']) > max_size:
                    max_size = size_types.index(item['type'])
                    url = item['url']

        return url, size_types[max_size]

    # Create file json from dictionary
    @staticmethod
    def add_json_file(path, file_dict):
        file = open(path, 'w', encoding='utf-8')
        file.writelines(json.dumps(file_dict, ensure_ascii=False, indent=2))


if __name__ == "__main__":

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        print(load_dotenv(dotenv_path))

    access_token = dotenv_values()['access_token']
    user_id = dotenv_values()['user_id']
    token_yandex_dick = dotenv_values()['token_yandex_dick']

    vk = VK(access_token, user_id)
    vk.create_backup_folder(token_yandex_dick)

    # To function is the number of photos (default five) and get the json-file
    photos = vk.users_photo()
    vk.keep_photo(photos, token_yandex_dick)
    vk.add_json_file('BackupPhotoInfo.json', vk.photo_json)
