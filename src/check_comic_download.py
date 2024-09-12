import os
import re
from rich import print


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


if __name__ == "__main__":
    download_path = "../Download"
    check_comic_pic_num(download_path)
