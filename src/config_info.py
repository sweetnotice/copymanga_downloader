import json
import os
from spider_toolbox import file_tools

with open('config.json', encoding='utf-8') as f:
    config = json.loads(f.read())
    download_path = config['下载路径']

if not os.path.isdir(download_path):
    file_tools.mkdir(download_path)
