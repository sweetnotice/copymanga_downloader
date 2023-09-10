import os
import time
from spider_toolbox import requests_tools, file_tools
from concurrent.futures import ThreadPoolExecutor
from src import drew_comment_pic


def download(url, workdir, name):
    resp = requests_tools.byte_downloader(url, workdir, name, 'jpg')
    workdir = os.path.join(workdir, name) + '.jpg'
    if resp:
        print(f'{workdir}下载完成\n', end='')
    else:
        print(f'{workdir} 下载出错')


class Comic_downloader:
    def __init__(self, comic_name, chapter_pic_comments):
        self.chapter_pic_comments = chapter_pic_comments

        comic_name = file_tools.format_str(comic_name)
        # 创建根目录
        file_tools.mkdir('Download')
        self.workdir = os.path.join('Download', comic_name)
        # 一级目录
        file_tools.mkdir(self.workdir)

    def downloader(self):
        for title, pic_comment_item in self.chapter_pic_comments.items():
            # 创建二级目录
            workdir = os.path.join(self.workdir, file_tools.format_str(title))
            file_tools.mkdir(workdir)
            with ThreadPoolExecutor(30) as f:
                pic_urls = pic_comment_item['pic_url']
                comments = pic_comment_item['comment']
                for i, pic_url in enumerate(pic_urls, start=1):
                    time.sleep(0.2)
                    # download(pic_url, workdir, i)
                    f.submit(download, pic_url, workdir, str(i))
                # 当前话的评论
                f.submit(drew_comment_pic.main, comments, workdir, str(i + 1))

    def main(self):
        self.downloader()
        print('下载完毕')


if __name__ == '__main__':
    ids = {'第01话': 'eec043de-f106-11e9-aab3-00163e0ca5bd', '第02话': '30bf03f4-170b-11ea-b69c-00163e0ca5bd',
           '第03话': '82b51cea-273a-11ea-a0fc-00163e0ca5bd', '第04话': '81ef6c3c-449c-11ea-9805-00163e0ca5bd',
           '第05话': '8e1b3b70-57f3-11ea-ba80-00163e0ca5bd', '情人节特别篇': '8e1b761c-57f3-11ea-ba80-00163e0ca5bd'}
    Comic_downloader(ids).main()
