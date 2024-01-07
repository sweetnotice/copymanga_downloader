import os
from rich import print
from spider_toolbox import requests_tools, file_tools


# @vthread.pool(20)
def download(url, workdir, name, info=False):
    resp = requests_tools.byte_downloader(url,
                                          workdir=workdir,
                                          file_name=name,
                                          file_type='jpg',
                                          timeout=3,
                                          retry_num=20,
                                          retry_sleep=1)
    workdir = os.path.join(workdir, name) + '.jpg'
    if info:
        if resp:
            print(f'[white]{workdir}下载完成[/]\n', end='')
        else:
            print(f'[red]{workdir} 下载出错[/]')


if __name__ == '__main__':
    download(r'https://hi77-overseas.mangafuna.xyz/gudubianji/cover/1651124428.jpg.328x422.jpg',
             r'C:\Users\Administrator\Desktop',
             '111')
