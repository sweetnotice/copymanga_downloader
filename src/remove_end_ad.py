import cv2
import os
import shutil
import numpy as np
from tqdm import tqdm
from rich import print
from concurrent.futures import ThreadPoolExecutor, as_completed
from spider_toolbox import file_tools


# 通过得到RGB每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    image1 = cv_imread(image1)
    image2 = cv_imread(image2)
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


def cv_imread(filePath):
    # 解决opencv读取中文路径报错的问题
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)

    # imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr
    # cv_img = cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img


# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def find_last_images(folder_path, last_num=-2):
    image_paths = []

    for root, dirs, files in os.walk(folder_path):
        if len(files) > -last_num:
            files = sorted(files, key=lambda x: int(x.split('.')[0]))
            second_last_image = files[last_num]
            image_paths.append(os.path.join(root, second_last_image))
    return image_paths


def contrast_pic(pic1, pic2):
    # 图片对比
    if os.path.isfile(pic1) and os.path.isfile(pic2) \
            and pic2 not in ad_pics:
        similarity = classify_hist_with_split(pic1, pic2)
        # cv_num += 1
        if similarity >= 0.83:
            # print(f'{pic1}\n{pic2}\n{similarity}\n')
            if pic1 not in ad_pics:
                ad_pics.append(pic1)
            if pic2 not in ad_pics:
                ad_pics.append(pic2)
        return pic1, pic2
    # print('111')


def find_ad_pics(pics):
    futures = []
    with ThreadPoolExecutor(15) as f:
        for pic1 in pics:
            for pic2 in pics[pics.index(pic1) + 1:]:
                futures.append(f.submit(contrast_pic, pic1, pic2))
        pbar = tqdm(total=len(futures), desc='识别汉化组广告中...')
        for future in as_completed(futures):
            # a = future.result()
            pbar.update()


class Del_pic_menu:
    def __init__(self, ad_pics):
        self.desktop_ad_path = None
        self.ad_pics = ad_pics

    def del_ad_pic(self):
        ad_lists = []
        # 从桌面文件夹中获取文件 文件夹里的文件名就是ad_pics中的序号
        for ad_pic_list in os.listdir(self.desktop_ad_path):
            ad_pic_list = int(ad_pic_list.replace('.jpg', ''))
            ad_lists.append(self.ad_pics[ad_pic_list])
        for ad_pic in ad_lists:
            os.remove(ad_pic)
        file_tools.del_dir(self.desktop_ad_path, mode=2)

    def save_pic_in_desktop(self):
        self.desktop_ad_path = os.path.join(file_tools.get_path(desktop=True), '广告')
        file_tools.mkdir(self.desktop_ad_path)
        for i, ad_pic in enumerate(self.ad_pics):
            shutil.copy(ad_pic, os.path.join(self.desktop_ad_path, f'{i}.jpg'))

    def main(self):
        print(f'找到[red]{len(self.ad_pics)}[/]张广告图')
        self.save_pic_in_desktop()
        user_choice = input('已保存在桌面  删除其中误判部分后回车>>>')
        if user_choice in ['Y', 'y', '']:
            self.del_ad_pic()
            print('删除成功!')


def main(workdir):
    if input('是否需要删除汉化组广告 (Y|n)>>>') not in ['y', 'Y', '']:
        return
    all_last_pic_2 = find_last_images(workdir, -2)
    all_last_pic_3 = find_last_images(workdir, -3)
    all_last_pic = all_last_pic_2 + all_last_pic_3
    find_ad_pics(all_last_pic)

    if len(ad_pics) >= 3:
        Del_pic_menu(ad_pics).main()
    else:
        print('没发现广告')
    print()


ad_pics = []
if __name__ == '__main__':
    workdir = r'D:\pythoncode\代码\爬\copymanga_downloader\Download\田所同學'
    # workdir = r'D:\pythoncode\代码\爬\copymanga_downloader\Download\神畫師JK與OL腐女'
    main(workdir)
