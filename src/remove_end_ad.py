import cv2
import os
import numpy as np
from tqdm import tqdm
from rich import print
from concurrent.futures import ThreadPoolExecutor, as_completed


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
        if len(files) > 1:
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


def del_ad_pic(ad_pics):
    for ad_pic in ad_pics:
        os.remove(ad_pic)





def main(workdir):
    all_last_pic_2 = find_last_images(workdir, -2)
    all_last_pic_3 = find_last_images(workdir, -3)
    all_last_pic = all_last_pic_2 + all_last_pic_3
    find_ad_pics(all_last_pic)

    if len(ad_pics) != 0:
        print(f'找到[red]{len(ad_pics)}[/]张广告图(准确度极高)  (Y删除,n取消,r进入查看模式)>>>', end='')
        user_choice = input()
        if user_choice in ['Y', 'y', '']:
            del_ad_pic(ad_pics)
            print('删除成功!')
        elif user_choice in ['r', 'R']:
            open_num = 0
            for ad_pic in ad_pics:
                os.startfile(ad_pic)
                open_num += 1
                if open_num != 0 and open_num % 15 == 0:
                    input('回车查看下十五张>>>')
            user_choice = input('要删除吗  (Y/n)>>>')
            if user_choice in ['Y', 'y', '']:
                del_ad_pic(ad_pics)
                print('删除成功!')
    else:
        print('没发现广告')
    print()


ad_pics = []
if __name__ == '__main__':
    workdir = r'D:\pythoncode\代码\爬\copymanga_downloader\Download\住在附近的菜菜子小姐'
    main(workdir)
