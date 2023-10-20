from urllib.parse import urlparse
from src import copymanga_parser, updata
import json


def init_url(url: str):
    # https://copymanga.site/comic/wufajujuedeta#
    if 'copymanga' in url:
        domain = urlparse(url).netloc
        path_word = url.split('/')[-1].replace('#', '')
    else:
        raise '你这输的啥?'
    print(f'域名:{domain}  |  关键词:{path_word}\n')
    return domain, path_word


def write_global_info(domain, path_word):
    write_dict = {"domain": domain, "path_word": path_word}
    with open('src/global_web_info.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(write_dict))


def print_art_fort():
    print("""\
 ██████╗ ██████╗ ██████╗ ██╗   ██╗     ██████╗ ██╗     
██╔════╝██╔═══██╗██╔══██╗╚██╗ ██╔╝     ██╔══██╗██║     
██║     ██║   ██║██████╔╝ ╚████╔╝      ██║  ██║██║     
██║     ██║   ██║██╔═══╝   ╚██╔╝       ██║  ██║██║     
╚██████╗╚██████╔╝██║        ██║███████╗██████╔╝███████╗
 ╚═════╝ ╚═════╝ ╚═╝        ╚═╝╚══════╝╚═════╝ ╚══════╝ by夕攘""")


def main():
    print_art_fort()
    # updata.locked()
    updata.main(26)
    while 1:
        url = input('输入漫画目录页网址>>>')
        # url = 'https://copymanga.site/comic/wufajujuedeta'
        # url = 'https://www.copymanga.site/comic/lianyuqingchang'
        domain, path_word = init_url(url)
        write_global_info(domain, path_word)
        copymanga_parser.Copy_manga_parser().main()


if __name__ == '__main__':
    main()
