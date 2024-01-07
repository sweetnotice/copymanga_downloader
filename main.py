from src import updata, config_info
from src.copymanga import copymanga_parser


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
    updata.main(42)
    print(
        f'下载路径: {config_info.download_path} | '
        f'解析线程数 : {config_info.parser_thread_num} | '
        f'下载线程数: {config_info.down_thread_num}')
    while 1:
        url = input('输入漫画目录页网址>>>')
        # url = 'https://copymanga.site/comic/wufajujuedeta'
        # url = 'https://www.copymanga.site/comic/lianyuqingchang'
        if 'copymanga' in url:
            copymanga_parser.Copy_manga_parser(url).main()


if __name__ == '__main__':
    main()
