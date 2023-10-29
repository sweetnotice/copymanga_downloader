import json
import os
from spider_toolbox import file_tools


def get_configs():
    with open('config.json', encoding='utf-8') as f:
        config = json.loads(f.read())
        download_path = config['下载路径(使用左斜杠)']
        down_thread_num = config['同时下载话']
        config_infos = {'download_path': download_path,
                        'down_thread_num': down_thread_num}

    if not os.path.isdir(download_path):
        file_tools.mkdir(download_path)
    return config_infos


config_infos = get_configs()

# 下载路径
download_path = config_infos['download_path']
# 下载线程数
down_thread_num = config_infos['down_thread_num']
