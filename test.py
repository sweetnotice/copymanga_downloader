import cv2
import os
from math import sqrt

def compare_images(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    hist1 = cv2.calcHist([gray1],[0],None,[256],[0,256])
    hist2 = cv2.calcHist([gray2],[0],None,[256],[0,256])

    degree = 0
    degree = cv2.compareHist(hist1,hist2,cv2.HISTCMP_CORREL)

    return degree

for root, dirs, files in os.walk('Download'):
    for f in files:
        img_path = os.path.join(root, f)
        img = cv2.imread(img_path)

        for root1, dirs1, files1 in os.walk('Download'):
            for f1 in files1:
                img_path1 = os.path.join(root1, f1)

                if img_path != img_path1:
                    img1 = cv2.imread(img_path1)

                    score = compare_images(img, img1)

                    if score > 0.9:
                       print('{} 和 {} 相似度为: {}'.format(img_path, img_path1, score))
