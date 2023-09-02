import re
from rich import print
from src import comic_downloader, copymanga_api


class Copy_manga_parser:
    def __init__(self):
        self.copy_manga_api = copymanga_api.Copymange_api()
        self.comic_detail = {}

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
            self.comic_detail[group_name] = comic_chapters_list
        # print(self.comic_detail)

    def user_choose(self):
        # 让用户输入下载范围
        chapter_index = 1
        chapters_infos = {}
        for group_name, detail_item in self.comic_detail.items():
            print(f'[yellow]{group_name}[/]')
            for detail_info in detail_item:
                print(f'{chapter_index}    {detail_info["name"]}    {detail_info["type"]}')
                chapters_infos[detail_info["name"]] = detail_info['id']
                chapter_index += 1
        user_input = input('\n0:全部下载\n数字-数字:下载指定话>>>')
        if user_input == '0' or user_input == '':
            down_chapters_infos = chapters_infos
        elif re.search(r'\d+-\d+', user_input):
            start: int = int(user_input.split('-')[0]) - 1
            finish: int = int(user_input.split('-')[1])
            if start > finish:
                raise '结束小于开始'
            down_chapters_infos = {k: v for k, v in
                                   list(chapters_infos.items())[start:finish]}
        else:
            raise '你输的什么玩意?'
        comic_downloader.Comic_downloader(down_chapters_infos).main()

    def main(self):
        self.parse_comic_detail()
        self.user_choose()


if __name__ == '__main__':
    Copy_manga_parser().main()