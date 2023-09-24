import os
import time
from rich import print
from spider_toolbox import requests_tools, file_tools
from concurrent.futures import ThreadPoolExecutor
from src import drew_comment_pic, check_comic_download
from src.config_info import download_path


def download(url, workdir, name):
    resp = requests_tools.byte_downloader(url,
                                          workdir=workdir,
                                          file_name=name,
                                          file_type='jpg',
                                          timeout=3,
                                          retry_num=20,
                                          retry_sleep=1)
    workdir = os.path.join(workdir, name) + '.jpg'
    if resp:
        print(f'[white]{workdir}下载完成[/]\n', end='')
    else:
        print(f'[red]{workdir} 下载出错[/]')


download_path = download_path


class Comic_downloader:
    def __init__(self, comic_name, chapter_pic_comments, start_chapter_index):
        self.chapter_pic_comments = chapter_pic_comments
        self.chapter_index = start_chapter_index  # 开始下载章节序号
        self.comic_name = file_tools.format_str(comic_name)
        # 创建根目录
        file_tools.mkdir(download_path)
        self.workdir = os.path.join(download_path, self.comic_name)
        # 一级目录
        file_tools.mkdir(self.workdir)

    def one_chapter_downloader(self, chapter_index, title, pic_comment_item, thread_num: 20):
        # 创建二级目录
        workdir = os.path.join(self.workdir, file_tools.format_str(f'{chapter_index}_{title}'))
        file_tools.mkdir(workdir)
        with ThreadPoolExecutor(thread_num) as f:
            pic_urls = pic_comment_item['pic_url']
            comments = pic_comment_item['comment']
            for i, pic_url in enumerate(pic_urls, start=1):
                # time.sleep(0.2)
                # download(pic_url, workdir, i)
                f.submit(download, pic_url, workdir, str(i))
            # 当前话的评论
            f.submit(drew_comment_pic.main, comments, workdir, str(i + 1))

    def thread_downloader(self, thread_num: int = 2):
        with ThreadPoolExecutor(thread_num) as ff:
            for title, pic_comment_item in self.chapter_pic_comments.items():
                ff.submit(self.one_chapter_downloader,
                          self.chapter_index,
                          title,
                          pic_comment_item,
                          20)
                self.chapter_index += 1

    def main(self):
        self.thread_downloader(thread_num=2)
        # 检查下载数量
        check_comic_download.check_comic_pic_num(self.workdir)


if __name__ == '__main__':
    ids = {'第01话': 'eec043de-f106-11e9-aab3-00163e0ca5bd', '第02话': '30bf03f4-170b-11ea-b69c-00163e0ca5bd',
           '第03话': '82b51cea-273a-11ea-a0fc-00163e0ca5bd', '第04话': '81ef6c3c-449c-11ea-9805-00163e0ca5bd',
           '第05话': '8e1b3b70-57f3-11ea-ba80-00163e0ca5bd', '情人节特别篇': '8e1b761c-57f3-11ea-ba80-00163e0ca5bd'}
    Comic_downloader(ids).main()
