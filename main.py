import requests


class VK:

    def __init__(self, access_token, user_id, version='5.131'):

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
        params = {'owner_id': self.id, 'album_id': 'wall', 'extended': '1','photo_sizes':'1'}
        response = requests.get(url, params={**self.params, **params})
        return  response.json()

if __name__ == "__main__":
    access_token = 'vk1.a.8VE5voNY1sHDUHPoyC34SnPmd-nYDKZ9A2-XHPAMOdUjCuqaOdZhOWeMCCs5tFeY5JXHcTWxzmTuUj5fdtmU87AEAhzfeWqg_Cj5B9gudXtogyVIUwMZ7Z7CAb5xz4ZQa_xcFQ7fhIcFRO64VtGSyICiFNghA-khA2DuKXTZ3nKosFLYVBaAXGEEQZKl7vse'
    user_id = '143235225'
    vk = VK(access_token, user_id)
    print(vk.users_photo())
    #print(vk.users_info())
