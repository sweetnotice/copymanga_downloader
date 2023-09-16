import os
import json


def get_config_info():
    config_info_ = {}
    with open('config.json', encoding='utf-8') as f:
        config = json.loads(f.read())
        config_info_['download_path'] = config['下载路径']
    return config_info_


config_info = get_config_info()
