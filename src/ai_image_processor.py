import os, subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time


def get_images(workdir):
    img_lists = []
    for root, dir, files in os.walk(workdir):
        if files:
            files = sorted(files, key=lambda x: int(x.split('.')[0]))
            for file in files[:-1]:
                img_path = os.path.join(root, file)
                img_lists.append(img_path)
    return img_lists


def processor(input_img, pbar, scale):
    exe_path = r'tool/realesrgan-ncnn-vulkan/realesrgan-ncnn-vulkan.exe'
    # exe_path = r'D:\pythoncode\代码\爬\copymanga_downloader\tool\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe'
    output_img = f'{input_img}_1.jpg'
    command = f'{exe_path} -i {input_img} -o {output_img} -s {scale}'
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # os.system(command)
    os.remove(input_img)
    os.rename(output_img, input_img)
    pbar.update()
    # print(f'{input_img} 优化成功')


def thread_launcher(img_lists, scale, thread_num):
    # 占用太高了
    # threading.Thread(target=processor, args=(input_img,
    #                                          scale)).start()
    pbar = tqdm(total=len(img_lists), desc='ai超分中...')
    with ThreadPoolExecutor(thread_num) as f:
        for img in img_lists:
            time.sleep(0.1)
            f.submit(processor,
                     img,
                     pbar,
                     scale)


def main(workdir, scale: int = 2, thread_num: int = 10):
    user_input = input('是否需要ai优化图片,可能会耗时比较长(Y|n)>>>')
    if user_input not in ['y', '', 'Y']:
        return
        # print(img_lists)
    img_lists = get_images(workdir)
    thread_launcher(img_lists,
                    scale,
                    5)


if __name__ == '__main__':
    # launcher(r'C:\Users\Administrator\Desktop\1647050818170007.jpg.c1500x.jpg')
    main(r'D:\漫画\金槍魚妹妹想被人吃掉')
