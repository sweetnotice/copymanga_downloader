import os
from spider_toolbox import file_tools
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from src import drew_comment_pic, check_comic_download, remove_end_ad, config_info, pic_downloader, ai_image_processor

download_path = config_info.download_path


class Comic_downloader:
    def __init__(self, comic_name, chapter_pic_comments):
        self.chapter_pic_comments = chapter_pic_comments
        self.comic_name = file_tools.format_str(comic_name)
        # 创建根目录 download目录
        file_tools.mkdir(download_path)
        # 一级目录 书目录
        self.workdir = os.path.join(download_path, self.comic_name)
        file_tools.mkdir(self.workdir)

    def one_chapter_downloader(self, title, pic_comment_item, thread_num: 20, pbar):
        # 创建二级目录 话目录
        workdir = os.path.join(self.workdir, file_tools.format_str(f'{title}'))
        file_tools.mkdir(workdir)
        with ThreadPoolExecutor(thread_num) as f:
            pic_urls = pic_comment_item['pic_url']
            comments = pic_comment_item['comment']
            for i, pic_url in enumerate(pic_urls, start=1):
                f.submit(pic_downloader.download, pic_url, workdir, str(i), False)
            # 当前话的评论
            drew_comment_pic.main(comments, workdir, str(i + 1))
        pbar.update()

    def thread_downloader(self):
        pbar = tqdm(total=len(self.chapter_pic_comments.items()), desc='漫画下载中...')
        with ThreadPoolExecutor(config_info.down_thread_num) as f:
            for title, pic_comment_item in self.chapter_pic_comments.items():
                f.submit(self.one_chapter_downloader,
                         title,
                         pic_comment_item,
                         20,
                         pbar)

    def main(self):
        self.thread_downloader()
        # 核对下载数量
        check_comic_download.check_comic_pic_num(self.workdir)
        # 删除汉化组广告
        remove_end_ad.main(self.workdir)
        # ai优化
        ai_image_processor.main(self.workdir)


if __name__ == '__main__':
    ids = {'第01话': 'eec043de-f106-11e9-aab3-00163e0ca5bd', '第02话': '30bf03f4-170b-11ea-b69c-00163e0ca5bd',
           '第03话': '82b51cea-273a-11ea-a0fc-00163e0ca5bd', '第04话': '81ef6c3c-449c-11ea-9805-00163e0ca5bd',
           '第05话': '8e1b3b70-57f3-11ea-ba80-00163e0ca5bd', '情人节特别篇': '8e1b761c-57f3-11ea-ba80-00163e0ca5bd'}
    Comic_downloader(ids).main()
