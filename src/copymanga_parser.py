import re
import os
from rich import print
from tqdm import tqdm
from src import comic_downloader, copymanga_api
from src.config_info import download_path


class Copy_manga_parser:
    def __init__(self):
        self.copy_manga_api = copymanga_api.Copymange_api()
        self.comic_name = self.copy_manga_api.get_comic_name()
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
                comic_chapter = {'name': chapter['name'],
                                 'type': comic_type[str(chapter['type'])],
                                 'id': chapter['id']}
                comic_chapters_list.append(comic_chapter)
                self.all_chapter_name_id[chapter['name']] = chapter['id']
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
        # 获取每话图片地址和评论 {话:{pic_url:[图片链接],comment:{用户名:评论}}}
        chapter_pic_comments = {}
        for chapter_title, chapter_id in tqdm(down_chapter_infos.items(), desc='漫画解析中...'):
            chapter_pic_comments[chapter_title] = {'pic_url': self.get_pic(chapter_id),
                                                   'comment': self.get_comment(chapter_id)}
        return chapter_pic_comments

    def main(self):
        self.parse_comic_detail()
        self.show_text()
        if self.is_downloaded():
            down_chapter_infos = self.user_choose()
            chapter_pic_comments = self.get_chapters_pic_comment(down_chapter_infos)
            comic_downloader.Comic_downloader(self.comic_name, chapter_pic_comments, self.start_chapter_index).main()


if __name__ == '__main__':
    Copy_manga_parser().main()
