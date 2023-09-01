import os
import time
import requests
from tqdm import tqdm
from Spider_Toolkit import spidertools
from src import copymanga_api, file_tool
from concurrent.futures import ThreadPoolExecutor


def download(url, workdir, name):
    # workdir = os.path.join(workdir, name) + '.jpg'
    # resp = requests.get(url, headers=copymanga_api.headers).content
    # with open(workdir, 'wb') as f:
    #     f.write(resp)
    spidertools.donwload_byte_function(url, path_=workdir, name=name, type_='.jpg')
    workdir = os.path.join(workdir, name) + '.jpg'
    print(f'{workdir}下载完成\n', end='')


class Comic_downloader:
    def __init__(self, domain, path_word, chapters_infos):
        self.copy_manga_api = copymanga_api.Copymange_api(domain, path_word)
        self.chapters_infos: dict = chapters_infos
        comic_name = file_tool.format_str(self.copy_manga_api.get_comic_name())
        self.workdir = comic_name
        file_tool.mkdir(comic_name)

    def get_chapters_pic(self) -> dict:
        # 获取每话图片地址 {话:[url链接]}
        chapter_pic_infos = {}
        for chapter_title, chapter_id in tqdm(self.chapters_infos.items(), desc='图片链接获取中...'):
            pic_lists = []
            pic_detail = self.copy_manga_api.get_comic_pics(chapter_id)
            for pic_item in pic_detail:
                pic_lists.append(pic_item['url'])
            chapter_pic_infos[chapter_title] = pic_lists
        return chapter_pic_infos

    def downloader(self, chapter_pic_infos: dict):
        for title, pic_lists in chapter_pic_infos.items():
            title = file_tool.format_str(title)
            workdir = os.path.join(self.workdir, title)
            file_tool.mkdir(workdir)
            with ThreadPoolExecutor(30) as f:
                for i, pic_url in enumerate(pic_lists, start=1):
                    time.sleep(0.1)
                    i = str(i)
                    # download(pic_url, workdir, i)
                    f.submit(download, pic_url, workdir, i)

    def main(self):
        chapter_pic_infos = self.get_chapters_pic()
        self.downloader(chapter_pic_infos)


if __name__ == '__main__':
    ids = {'第01话': 'eec043de-f106-11e9-aab3-00163e0ca5bd', '第02话': '30bf03f4-170b-11ea-b69c-00163e0ca5bd',
           '第03话': '82b51cea-273a-11ea-a0fc-00163e0ca5bd', '第04话': '81ef6c3c-449c-11ea-9805-00163e0ca5bd',
           '第05话': '8e1b3b70-57f3-11ea-ba80-00163e0ca5bd', '情人节特别篇': '8e1b761c-57f3-11ea-ba80-00163e0ca5bd'}
    Comic_downloader('copymanga.site', 'wufajujuedeta', ids).main()