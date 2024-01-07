import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from tqdm import tqdm


def get_avg_resolution(img_lists):
    def get_resolution(image_path):
        # 查看清晰度
        img = Image.open(image_path)
        width, height = img.size
        return width, height

    import random
    random_img = random.sample(img_lists, int(len(img_lists) / 2))  # 随机取图片
    resolution_list = [get_resolution(i) for i in random_img]
    widths = [width for width, height in resolution_list]
    heights = [height for width, height in resolution_list]

    total_width = sum(widths)
    total_height = sum(heights)
    avg_width = int(total_width / len(random_img))
    avg_height = int(total_height / len(random_img))
    if avg_width * avg_height <= 420000:
        pic_lv = '低,建议优化'
    elif avg_width * avg_height <= 800000:
        pic_lv = '中,可选优化'
    else:
        pic_lv = '高,无需优化'
    avg_resolution = (avg_width, avg_height)
    # print(total_width)
    # print(total_height)
    # print(avg_resolution)
    return avg_resolution, pic_lv


def get_images(workdir):
    img_lists = []
    for root, dir, files in os.walk(workdir):
        if files:
            files = sorted(files, key=lambda x: int(x.split('.')[0]))
            for file in files[:-1]:
                img_path = os.path.join(root, file)
                img_lists.append(img_path)
    return img_lists


def processor(input_img, scale, pbar):
    exe_path = r'tool/realesrgan-ncnn-vulkan/realesrgan-ncnn-vulkan.exe'
    # exe_path = r'D:\pythoncode\代码\爬\copymanga_downloader\tool\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe'
    output_img = f'{input_img}_1.jpg'
    command = f'{exe_path} -i {input_img} -o {output_img} -s {scale} -j 4:4:4'
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # os.system(command)
    os.remove(input_img)
    os.rename(output_img, input_img)
    pbar.update()
    # print(f'{input_img} 优化成功')


def thread_launcher(img_lists, scale, thread_num):
    pbar = tqdm(total=len(img_lists), desc='ai超分中...')
    with ThreadPoolExecutor(thread_num) as f:
        for img in img_lists:
            time.sleep(0.1)
            f.submit(processor,
                     img,
                     scale,
                     pbar)


def main(workdir, scale: int = 2, thread_num: int = 10):
    img_lists = get_images(workdir)
    avg_resolution = get_avg_resolution(img_lists)
    user_input = input(
        f'平均像素{avg_resolution[0]} {avg_resolution[1]}\n'
        f'是否需要ai优化图片,预计耗时{int(len(img_lists) / 60)}min (Y|n)>>>')
    if user_input not in ['y', '', 'Y']:
        return
        # print(img_lists)

    thread_launcher(img_lists,
                    scale,
                    4)


if __name__ == '__main__':
    # launcher(r'C:\Users\Administrator\Desktop\1647050818170007.jpg.c1500x.jpg')
    # main(r'C:\Users\Administrator\Desktop\好一個變態')
    main(r'D:\漫画\海貓鳴泣之時EP3')
    # avg_resolution(get_images(r'C:\Users\Administrator\Desktop\好一個變態'))
