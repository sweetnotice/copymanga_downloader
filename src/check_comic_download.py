import os
import re
from rich import print
from pathlib import Path


def check_comic_pic_num(workdir):
    lose_pic_dirs = []
    for root, dirs, files in os.walk(workdir):
        if files:
            files.sort(key=lambda x: int(re.findall(r"(\d+).jpg", x)[0]))
            if len(files) != int(files[-1].replace(".jpg", "")):
                lose_pic_dirs.append(root)
    if len(lose_pic_dirs) == 0:
        print("[green]下载完毕 无缺失页[/]")
    else:
        print(f"[red]{lose_pic_dirs} 话图片缺失![/]")
    print()


def check_is_down(manga_name, down_dir):
    # 检查是否下载过
    down_lists = Path(down_dir).iterdir()
    for down_manga in down_lists:
        if manga_name == down_manga.stem:
            print(f'\n{manga_name} 下载过了！')
            input_ = input('是否要删除(N|y)>>>')
            if input_ in ['N', 'n', '']:
                return False
            else:
                down_manga.unlink()
                return True
    return True


if __name__ == "__main__":
    # download_path = "../Download"
    # check_comic_pic_num(download_path)
    check_is_down('迷宮干', r'X:\漫画')
