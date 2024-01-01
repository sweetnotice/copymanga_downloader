import os, subprocess
import threading


def processor(input_img, scale: int = 2):
    exe_path = r'tool/realesrgan-ncnn-vulkan/realesrgan-ncnn-vulkan.exe'
    # exe_path = r'D:\pythoncode\代码\爬\copymanga_downloader\tool\realesrgan-ncnn-vulkan\realesrgan-ncnn-vulkan.exe'
    output_img = f'{input_img}_1.jpg'
    command = f'{exe_path} -i {input_img} -o {output_img} -s {scale}'
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with open(input_img, 'wb') as f, open(output_img, 'rb') as ff:
        process_bite = ff.read()
        f.write(process_bite)
    os.remove(output_img)
    # print(f'{input_img} 优化成功')


def launcher(input_img, scale: int = 2):
    # 占用太高了
    threading.Thread(target=processor, args=(input_img,
                                             scale)).start()


if __name__ == '__main__':
    launcher(r'C:\Users\Administrator\Desktop\1.jpg')
