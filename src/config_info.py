import json
import os
from spider_toolbox import file_tools


def get_configs():
    with open("config.json", encoding="utf-8") as f:
        config = json.loads(f.read())
        download_path = config["下载路径(使用左斜杠)"]
        config_infos = {
            "download_path": config["下载路径(使用左斜杠)"],
            "parser_thread_num": config["同时解析话"],
            "down_thread_num": config["同时下载话"],
            "down_file_format": config["输出格式(jpg|cbz)"],
            "detect_ad_img": config["识别汉化组广告(true|false)"]
        }

    if not os.path.isdir(download_path):
        file_tools.mkdir(download_path)
    return config_infos


config_infos = get_configs()

# 下载路径
download_path: str = config_infos["download_path"]
# 解析话线程数
parser_thread_num: int = config_infos["parser_thread_num"]
# 下载线程数
down_thread_num: int = config_infos["down_thread_num"]
# 下载输出格式
down_file_format: str = config_infos["down_file_format"]
# 识别汉化组广告
detect_ad_img: bool = config_infos["detect_ad_img"]
pass
