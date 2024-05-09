import requests
import datetime
import json
from tqdm import tqdm as Bar

class VK:

    def __init__(self, access_token, user_id, version='5.131'):

        self.photo_json = {'items': []}
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):

        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})

        return response.json()

    def users_photo(self):

        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'wall', 'extended': '1', 'photo_sizes': '1', 'count': '7'}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def add_backup_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        token = 'y0_AgAAAABAqmI4AADLWwAAAAEEQT9fAACpwhq347ZKuKCK2HDSuT8xmbSSYA'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        params = {'path': 'Backup_Photo_BK'}
        requests.put(url, params={**params}, headers=headers)


    def keep_photo(self, photos):
        bank_likes = set()
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        token = 'y0_AgAAAABAqmI4AADLWwAAAAEEQT9fAACpwhq347ZKuKCK2HDSuT8xmbSSYA'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        bar = Bar(total=len(photos['response']['items']), desc="Loading…", ascii=False, ncols=100)
        for item in photos['response']['items']:
            if item['likes']['count'] in bank_likes:
                date = datetime.datetime.fromtimestamp(int(item['date']))
                photo_name = f'{item['likes']['count']}({date.date()}).jpg'
            else:
                photo_name = f'{item['likes']['count']}.jpg'
                bank_likes.add(item['likes']['count'])
            params_photo = self.best_size(item['sizes'])
            params = {'path': f'Backup_Photo_BK/{photo_name}', 'url': params_photo[0]}
            requests.post(url, params={**params}, headers=headers)
            self.photo_json['items'].append({'file_name': photo_name, 'size': params_photo[1]})
            bar.update(1)

    def best_size(self, sizes):
        url = ''
        size_types = ['s', 'm', 'x', 'o', 'p', 'q', 'r', 'y', 'z', 'w']
        max_size = 0
        for item in sizes:
            if item['type'] in size_types:
                if size_types.index(item['type']) > max_size:
                    max_size = size_types.index(item['type'])
                    url = item['url']
        return url, size_types[max_size]


    #def photo_save_info(self,file_name, size):



if __name__ == "__main__":
    access_token = 'vk1.a.AR5-1Pp-blXdr2gR7cgtYm2OnRAtQPhPwSvvZmkGimC_M5q44CEA2q9t0IZIUO9NQPeCt1zgZLTJCFmQDio_WUFN7csw_KFtqYDCJJ-lNye_gCAL638g_SzhyFRqH1H0w18IRz6pYDhk2t-sJfaRQwYymTb44aTE_QW3iWgxkYm9BuSOl1CtpOlFqpW2DKiX'
    user_id = '143235225'
    vk = VK(access_token, user_id)
    vk.add_backup_folder()
    vk.keep_photo(vk.users_photo())
    file = open('BackupPhotoInfo.json', 'w', encoding='utf-8')
    file.writelines(json.dumps(vk.photo_json, ensure_ascii=False, indent=2))
    #file =
    #print(file)
    #print(vk.users_info())
    #print(vk.keep_photo(file['response']['items'][0]['sizes'][5]['url']))
    #print(file['response']['items'][0]['sizes'][5]['url'])
