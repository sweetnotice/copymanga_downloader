import os
import time
from tqdm import tqdm
from Spider_Toolkit import spidertools
from src import file_tool, drew_comment_pic, copymanga_api
from concurrent.futures import ThreadPoolExecutor


def download(url, workdir, name):
    spidertools.donwload_byte_function(url, path_=workdir, name=name, type_='.jpg')
    workdir = os.path.join(workdir, name) + '.jpg'
    print(f'{workdir}下载完成\n', end='')


class Comic_downloader:
    def __init__(self, chapters_infos):
        self.copy_manga_api = copymanga_api.Copymange_api()
        self.chapters_infos: dict = chapters_infos
        comic_name = file_tool.format_str(self.copy_manga_api.get_comic_name())
        # 创建根目录
        file_tool.mkdir('Download')
        self.workdir = os.path.join('Download', comic_name)
        # 一级目录
        file_tool.mkdir(self.workdir)

    def get_comment(self, chapter_id):
        # 获取一话评论
        comment_lists = []
        comment_detail = self.copy_manga_api.get_chapter_comment(chapter_id)
        for comment_item in comment_detail:
            comment_lists.append(comment_item['comment'])
        return comment_lists

    def get_pic(self, chapter_id):
        # 获取一话图片
        pic_lists = []
        pic_detail = self.copy_manga_api.get_comic_pics(chapter_id)
        for pic_item in pic_detail:
            pic_lists.append(pic_item['url'])
        return pic_lists

    def get_chapters_pic_comment(self):
        # 获取每话图片地址 {话:[图片链接]}
        chapter_pic_infos = {}
        chapter_comments_infos = {}
        for chapter_title, chapter_id in tqdm(self.chapters_infos.items(), desc='漫画解析中...'):
            chapter_pic_infos[chapter_title] = self.get_pic(chapter_id)
            chapter_comments_infos[chapter_title] = self.get_comment(chapter_id)
        return chapter_pic_infos, chapter_comments_infos

    def downloader(self, chapter_pic_infos: dict, chapter_comments_infos: dict):
        chapter_index = 1
        for title, pic_lists in chapter_pic_infos.items():
            title = file_tool.format_str(title)
            # 创建二级目录
            workdir = os.path.join(self.workdir, title)
            file_tool.mkdir(workdir)
            with ThreadPoolExecutor(30) as f:
                for i, pic_url in enumerate(pic_lists, start=1):
                    time.sleep(0.08)
                    # download(pic_url, workdir, i)
                    f.submit(download, pic_url, workdir, str(i))
                # 当前话的评论
                comment_list: list = list(chapter_comments_infos.values())[chapter_index - 1]
                f.submit(drew_comment_pic.main, comment_list, workdir, str(i + 1))
            chapter_index += 1

    def main(self):
        chapter_pic_infos, chapter_comments_infos = self.get_chapters_pic_comment()
        self.downloader(chapter_pic_infos, chapter_comments_infos)
        print('下载完毕')


if __name__ == '__main__':
    ids = {'第01话': 'eec043de-f106-11e9-aab3-00163e0ca5bd', '第02话': '30bf03f4-170b-11ea-b69c-00163e0ca5bd',
           '第03话': '82b51cea-273a-11ea-a0fc-00163e0ca5bd', '第04话': '81ef6c3c-449c-11ea-9805-00163e0ca5bd',
           '第05话': '8e1b3b70-57f3-11ea-ba80-00163e0ca5bd', '情人节特别篇': '8e1b761c-57f3-11ea-ba80-00163e0ca5bd'}
    Comic_downloader(ids).main()