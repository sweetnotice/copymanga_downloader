from urllib.parse import urlparse
from src import copymanga_parser


def init_url(url: str):
    # https://copymanga.site/comic/wufajujuedeta
    if 'copymanga' in url:
        domain = urlparse(url).netloc
        path_word = url.split('/')[-1]
    else:
        raise '你这输的啥?'
    print(f'域名:{domain}  |  关键词:{path_word}\n')
    return domain, path_word


def main():
    while 1:
        url = input('输入漫画目录页网址>>>')
        # url = 'https://copymanga.site/comic/wufajujuedeta'
        domain, path_word = init_url(url)
        copymanga_parser.Copy_manga_parser(domain=domain, path_word=path_word).main()


if __name__ == '__main__':
    main()