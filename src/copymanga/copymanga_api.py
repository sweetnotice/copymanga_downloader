import re
from spider_toolbox import requests_tools
from src.copymanga import result_decrypt

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}


class Copymange_api:
    def __init__(self, domain, path_word):
        self.domain, self.path_word = domain, path_word
        self.retry_num = 10
        self.timeout = 3

    def get_comic_name(self):
        resp = requests_tools.get(f'https://{self.domain}/comic/{self.path_word}', headers=headers,
                                  timeout=self.timeout, retry_num=self.retry_num)
        if resp.status_code != 200:
            raise '请检查网络连接'
        comic_name = re.search('<h6 title="(.*?)">.*?</h6>', resp.text).group(1)
        return comic_name

    def get_comicdetail(self):
        resp = requests_tools.get(f'https://{self.domain}/comicdetail/{self.path_word}/chapters', headers=headers,
                                  timeout=self.timeout, retry_num=self.retry_num)
        if resp.status_code != 200:
            raise '请检查网络连接'
        if resp.json()['code'] != 200:
            raise resp.json()['message']
        encrypt_data = resp.json()['results']
        decrypt_data = result_decrypt.mange_decrypt(encrypt_data)
        # print(decrypt_data)
        return decrypt_data

    def get_comic_pics(self, chapter_id):
        resp = requests_tools.get(f'https://{self.domain}/comic/{self.path_word}/chapter/{chapter_id}', headers=headers,
                                  timeout=self.timeout, retry_num=self.retry_num)
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
        resp = requests_tools.get(
            f'https://api.{domain}/api/v3/roasts?chapter_id={chapter_id}&limit=50&offset=0&_update=true',
            headers=headers,
            timeout=self.timeout, retry_num=self.retry_num)
        if resp.status_code != 200:
            raise '请检查网络连接'
        if resp.json()['code'] != 200:
            raise resp.json()['message']
        return resp.json()['results']['list']
