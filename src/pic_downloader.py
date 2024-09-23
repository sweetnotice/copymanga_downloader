import os
import requests
from spider_toolbox import requests_tools


def download(url, workdir, name, info=False):
    downloader(
        url=url,
        workdir=workdir,
        file_name=name,
        file_type="jpg",
    )


@requests_tools.retry_on_exception(10)
def downloader(url, file_name, file_type, workdir):
    file_type = file_type.replace('.', '')
    workdir = os.path.join(workdir, file_name) + '.' + file_type
    resp = requests.get(url)
    if resp:
        with open(workdir, 'wb') as f:
            f.write(resp.content)


if __name__ == "__main__":
    download(
        r"https://hi77-overseas.mangafuna.xyz/gudubianji/cover/1651124428.jpg.328x422.jpg",
        r"C:\Users\Administrator\Desktop",
        "111",
    )
