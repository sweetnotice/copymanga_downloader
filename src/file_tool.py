import os
from rich import print


# 格式化为可以创建的文件名
def format_str(data: str):
    # 去除字符串中的 ' / , \ , " , ? , * , < , > , | , : ,空格'
    return data.replace('/', '').replace('\\', '').replace('"', '').replace('?', '').replace('*', '') \
        .replace('<', '').replace('>', '').replace('|', '').replace(':', '').replace(' ', '')


# 创建文件夹
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if isExists := os.path.exists(path):
        # print(' 创建过了')
        return False
    os.makedirs(path)
    print(f'[yellow]{path} 创建成功[/]')
    return True