import requests, os


def main(commit_num):
    print('检查更新中...', end='')
    resp = requests.get('https://api.github.com/repos/sweetnotice/copymanga_downloader/commits').json()
    if len(resp) > commit_num:
        print('\r有更新了  https://github.com/sweetnotice/copymanga_downloader 点击查看', flush=True)
    else:
        print('\r软件已经是最新版!', flush=True)


def locked():
    password_file = 'password.pwd'
    while 1:
        if os.path.isfile(password_file):
            with open(password_file, 'r', encoding='utf-8') as f:
                password = f.read()
        else:
            password = input('输入密码>>>')
        if password == '330660':
            with open(password_file, 'w', encoding='utf-8') as f:
                f.write(str(password))
            break
        else:
            print('密码错误!')


if __name__ == '__main__':
    # main(24)
    locked()
