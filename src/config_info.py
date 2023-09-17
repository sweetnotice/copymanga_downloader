import json

config_info = {}
with open('config.json', encoding='utf-8') as f:
    config = json.loads(f.read())
    config_info['download_path'] = config['下载路径']
