import requests


def main(commit_num):
    print("检查更新中...", end="")
    try:
        resp = requests.get(
            "https://api.github.com/repos/sweetnotice/copymanga_downloader/commits?per_page=1000",
            timeout=3,
        ).json()
        if len(resp) > commit_num:
            print(
                "\r有更新了  https://github.com/sweetnotice/copymanga_downloader 点击查看",
                flush=True,
            )
        else:
            print("\r软件已经是最新版!", flush=True)
    except Exception:
        print("\r更新获取失败!", flush=True)


if __name__ == "__main__":
    main(42)
    # locked()
