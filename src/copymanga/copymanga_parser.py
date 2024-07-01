import re
import os
from concurrent.futures import ThreadPoolExecutor
from rich import print
from tqdm import tqdm
from urllib.parse import urlparse
from src.copymanga import copymanga_api, copymanga_comic_downloader
from src.config_info import download_path, parser_thread_num
from spider_toolbox.file_tools import format_str


def del_str_special_words(text):
    text = re.sub('[^A-Za-z0-9\u4e00-\u9fff_.]+', '', text)
    return text


def parse_input_url(url):
    # https://copymanga.site/comic/wufajujuedeta#
    path_word = url.split('/')[-1].replace('#', '')
    domain = urlparse(url).netloc
    print(f'域名:{domain}  |  关键词:{path_word}\n')
    return domain, path_word


class Copy_manga_parser:
    def __init__(self, url):
        domain, path_word = parse_input_url(url)
        self.copy_manga_api = copymanga_api.Copymange_api(domain, path_word)
        self.comic_name = format_str(self.copy_manga_api.get_comic_name())
        self.comic_detail = {'默认': [{'name': '第一话', 'type': '话', 'id': 'id'}]}
        self.all_chapter_name_id = {'第一话': 'id', '第二话': 'id'}
        self.comic_detail, self.all_chapter_name_id = {}, {}
        self.start_chapter_index = 1  # 选择开始下载章节的序号

    def parse_comic_detail(self):
        # 解析漫画章节
        detail = self.copy_manga_api.get_comicdetail()
        # {1: '話', 2: '卷', 3: '番外篇'}
        comic_type = {str(i["id"]): i["name"] for i in detail['build']['type']}
        for item in detail['groups'].values():
            comic_chapters_list = []
            group_name = item['name']
            for chapter in item['chapters']:
                comic_chapter = {'name': format_str(chapter['name']),
                                 'type': comic_type[str(chapter['type'])],
                                 'id': chapter['id']}
                comic_chapters_list.append(comic_chapter)
                self.all_chapter_name_id[format_str(chapter['name'])] = chapter['id']
            self.comic_detail[group_name] = comic_chapters_list

        # print(self.comic_detail)

    def show_text(self):
        i = 1
        print(self.comic_name)
        for group_name, detail_item in self.comic_detail.items():
            print(f'[yellow]{group_name}[/]')
            for detail_info in detail_item:
                print(f'{i}    {detail_info["name"]}    {detail_info["type"]}')
                i += 1

    def is_downloaded(self):
        if self.comic_name in os.listdir(download_path):
            print('[red]已经下载过了,请问是否还要继续?(y/N)[/]', end='')
            choice = input('')
            if choice in ['Y', 'y']:
                return True
            elif choice in ['N', 'n', ' ']:
                return False
        return True

    def user_choose(self) -> dict:
        # 让用户输入下载范围 {'第一话':'id'}
        user_input = input('\n0:全部下载\n数字-数字:下载指定话>>>')
        if user_input == '0' or user_input == '':
            down_chapters_infos = self.all_chapter_name_id
        elif re.search(r'\d+-\d+', user_input):
            start: int = int(user_input.split('-')[0]) - 1
            finish: int = int(user_input.split('-')[1])
            if start > finish:
                raise '结束小于开始'
            down_chapters_infos = {k: v for k, v in
                                   list(self.all_chapter_name_id.items())[start:finish]}
            self.start_chapter_index = start + 1
        else:
            raise '你输的什么玩意?'
        return down_chapters_infos

    def get_comment(self, chapter_id) -> dict:
        # 获取一话评论  {用户名:评论}
        comment_items = {}
        comment_detail = self.copy_manga_api.get_chapter_comment(chapter_id)
        # comment_detail.reverse()  # 按照评论发布顺序排列  评论者似乎是从下往上的 楼上全部变成了楼下
        for comment_item in comment_detail:
            comment_user_name = comment_item['user_name']
            comment_data = comment_item['comment']
            comment_items[comment_user_name] = comment_data
        return comment_items

    def get_pic(self, chapter_id) -> list:
        # 获取一话图片
        pic_lists = []
        pic_detail = self.copy_manga_api.get_comic_pics(chapter_id)
        for pic_item in pic_detail:
            pic_lists.append(pic_item['url'])
        return pic_lists

    def get_chapters_pic_comment(self, down_chapter_infos: dict):
        # 获取每话图片地址和评论 {序号_话名:{pic_url:[图片链接],comment:{用户名:评论}}}
        def get_chapters_pic_comment_func(chapter_id, index, chapter_title, pic_comments_dict: dict, pbar):
            pic_comments_dict[f'{index}_{chapter_title}'] = \
                {'pic_url': self.get_pic(chapter_id),
                 'comment': self.get_comment(chapter_id)}
            pbar.update()

        chapter_pic_comments = {}
        pbar = tqdm(total=len(down_chapter_infos), desc='漫画解析中...')
        with ThreadPoolExecutor(parser_thread_num) as f:
            for chapter_title, chapter_id in down_chapter_infos.items():
                f.submit(get_chapters_pic_comment_func,
                         chapter_id,
                         self.start_chapter_index,
                         chapter_title,
                         chapter_pic_comments,
                         pbar)
                self.start_chapter_index += 1
        return chapter_pic_comments

    def main(self):
        self.parse_comic_detail()
        self.show_text()
        if self.is_downloaded():
            # 需要下载的话合集 {name:id}
            down_chapter_infos = self.user_choose()
            chapter_pic_comments = self.get_chapters_pic_comment(down_chapter_infos)
            copymanga_comic_downloader.Comic_downloader(self.comic_name, chapter_pic_comments).main()


if __name__ == '__main__':
    Copy_manga_parser().main()
