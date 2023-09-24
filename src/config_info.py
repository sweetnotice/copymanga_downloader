import json
import os
from spider_toolbox import file_tools


def get_configs():
    with open('config.json', encoding='utf-8') as f:
        config = json.loads(f.read())
        download_path = config['下载路径']
        config_infos = {'download_path': download_path}

    if not os.path.isdir(download_path):
        file_tools.mkdir(download_path)
    return config_infos


config_infos = get_configs()

download_path = config_infos['download_path']
