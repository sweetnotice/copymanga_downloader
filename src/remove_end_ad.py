# -*- coding: utf-8 -*-
import shutil
import os
import cv2
import numpy as np
from tqdm import tqdm


# 通过得到RGB每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
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


def copy_file_now_dir(file_path, save_name):
    # 复制图片到当前目录
    save_name += '.jpg'
    save_path = os.path.join(cwd, save_name)
    shutil.copy(file_path, save_path)


def get_last_3_pic(workdir):
    file_lists = sorted(os.listdir(workdir), key=lambda x: int(x.split('.')[0]))
    # 不包含最后的评论页
    last_3_pic = [os.path.join(workdir, file) for file in file_lists[-4:-1]]
    return last_3_pic


def remove_tqdm_pic():
    pics = ['0.jpg', '1.jpg', '2.jpg', '4.jpg']
    for pic in pics:
        os.remove(os.path.join(cwd, pic))


def compare_images(img1, img2):
    # 初始化SIFT检测器
    sift = cv2.SIFT_create()

    # 提取关键点和描述子
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # 匹配描述子
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # ratio test作为过滤条件
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # 计算匹配点对应率
    num_matches = len(good_matches)
    if len(kp1) > len(kp2):
        num_keypoints = len(kp1)
    else:
        num_keypoints = len(kp2)
    score = num_matches / num_keypoints

    return score


def get_ad_pics(chapter_lists):
    ad_pics = []
    for chapter in tqdm(chapter_lists, desc='查找汉化组广告中...'):
        for pic_ in get_last_3_pic(os.path.join(manga_dir, chapter)):
            copy_file_now_dir(pic_, '4')
            for i in range(3):
                img1 = cv2.imread(f'{i}.jpg')
                img2 = cv2.imread('4.jpg')
                n = classify_hist_with_split(img1, img2)
                if n >= 0.85 or n == 1.0:
                    # print(f'{pic_}这张图大概率是重复的')
                    ad_pics.append(pic_)
                    break
                # print(f'{i}三直方图算法相似度：', n)
    remove_tqdm_pic()
    return ad_pics


def del_ad_pic(del_list):
    for pic in del_list:
        os.remove(pic)


def main(workdir):
    global manga_dir
    if len(os.listdir(workdir)) <= 2:
        return
    manga_dir = workdir
    chapter_lists = sorted(os.listdir(workdir), key=lambda x: int(x.split('_')[0]))

    # 获取列表第二个的最后三张图并保存
    for i, pic_ in enumerate(get_last_3_pic(os.path.join(workdir, chapter_lists[1]))):
        copy_file_now_dir(pic_, str(i))

    # 获取相似度高的图片列表
    ad_pics = get_ad_pics(chapter_lists[2:])
    if len(ad_pics) >= 3:
        user_choice = input(f'将会删除{ad_pics}\n检查无误按下(Y|n)>>>')
        if user_choice in ['Y', 'y', ' ']:
            del_ad_pic(ad_pics)


# 输入的漫画的目录
manga_dir = ''
cwd = os.getcwd()
if __name__ == "__main__":
    main(r'D:\pythoncode\代码\爬\copymanga_downloader\Download\我想弄哭你')
