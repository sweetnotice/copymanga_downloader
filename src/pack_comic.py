import os
import zipfile


def zip_dir(folder_path, output_zip_path):
    """
    将指定文件夹压缩成zip文件。

    :param folder_path: 要压缩的文件夹路径
    :param output_zip_path: 输出的ZIP文件路径
    """
    # 创建一个ZipFile对象，并设置模式为w（写入）
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 构建完整的文件路径
                file_path = str(os.path.join(root, file))
                # 在ZIP文件中存储文件，使用相对路径
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


def pack_cbz(folder_path, output_zip_path):
    from pathlib import Path
    from cbz.comic import ComicInfo
    from cbz.constants import PageType, YesNo, Manga, AgeRating, Format
    from cbz.page import PageInfo

    chapters = list(Path(folder_path).iterdir())
    chapters = sorted(chapters, key=lambda x: int(x.name.split('_')[0]))
    pages = []
    for chapter in chapters:
        imgs = list(Path(chapter).iterdir())
        imgs = sorted(imgs, key=lambda x: int(x.stem))
        for i, img_path in enumerate(imgs):
            if i == 0:
                type = PageType.FRONT_COVER  # 封面
            else:
                if i == len(imgs) - 1:
                    type = PageType.BACK_COVER  # 尾页
                else:
                    type = PageType.STORY  # 内容页
            pages.append(PageInfo.load(path=img_path, type=type))

    # Create a ComicInfo object using ComicInfo.from_pages() method
    comic = ComicInfo.from_pages(
        pages=pages,
        title=os.path.basename(folder_path),
        series='Your Comic Series',
        number=1,
        format=Format.WEB_COMIC,
        black_white=YesNo.NO,
        manga=Manga.NO,
        age_rating=AgeRating.PENDING
    )

    # Show the comic using the show()
    # comic.show()

    # Pack the comic book content into a CBZ file format
    cbz_content = comic.pack()

    # Define the path where the CBZ file will be saved
    cbz_path = Path(output_zip_path)

    cbz_path.write_bytes(cbz_content)


if __name__ == '__main__':
    pack_cbz(r'D:\pythoncode\代码\爬\copymanga_downloader\聖癖✟櫻之丘', r'D:\pythoncode\代码\爬\copymanga_downloader\聖癖✟櫻之丘.cbz')
