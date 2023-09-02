import re
import requests
from src import result_decrypt, global_web_info

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}


class Copymange_api:
    def __init__(self):
        self.domain = global_web_info.domain
        self.path_word = global_web_info.path_word

    def get_comic_name(self):
        resp = requests.get(f'https://{self.domain}/comic/{self.path_word}', headers=headers)
        if resp.status_code != 200:
            raise '请检查网络连接'
        comic_name = re.search('<h6 title="(.*?)">.*?</h6>', resp.text).group(1)
        return comic_name

    def get_comicdetail(self):
        resp = requests.get(f'https://{self.domain}/comicdetail/{self.path_word}/chapters', headers=headers)
        if resp.status_code != 200:
            raise '请检查网络连接'
        if resp.json()['code'] != 200:
            raise resp.json()['message']
        encrypt_data = resp.json()['results']
        decrypt_data = result_decrypt.mange_decrypt(encrypt_data)
        # print(decrypt_data)
        return decrypt_data

    def get_comic_pics(self, chapter_id):
        resp = requests.get(f'https://{self.domain}/comic/{self.path_word}/chapter/{chapter_id}', headers=headers)
        if resp.status_code != 200:
            raise '请检查网络连接'
        encrypt_data = re.search('<div.class="imageData".contentKey="(.*?)"></div>', resp.text).group(1)
        decrypt_data = result_decrypt.mange_decrypt(encrypt_data)
        return decrypt_data

    def get_chapter_comment(self, chapter_id) -> list:
        # 获取话评论
        params = {
            'chapter_id': chapter_id,
            'limit': '50',
            'offset': '0',
            '_update': 'true',
        }
        domain = self.domain.replace('www.', '')
        resp = requests.get(f'https://api.{domain}/api/v3/roasts', params=params, headers=headers)
        if resp.status_code != 200:
            raise '请检查网络连接'
        if resp.json()['code'] != 200:
            raise resp.json()['message']
        return resp.json()['results']['list']