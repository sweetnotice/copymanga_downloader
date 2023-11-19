import os
from PIL import Image, ImageDraw, ImageFont


def parse_comment_item(comment_item: dict) -> list:
    """
    :param comment_item: {用户名:评论}
    :return:
    """
    comment_list = []
    for k, v in comment_item.items():
        v = v.replace("，", ",")
        comment = f'{k} : {v}'
        if len(comment) <= 45:
            comment_list.append(comment)
    if len(comment_list) == 0:
        comment_list.append('暂无评论...')
    return comment_list


def text_to_image(text_list, workdir, save_name,
                  font_path='msyh.ttc',
                  fontsize=16,
                  color=(0, 0, 0),
                  background=(255, 255, 255)):
    workdir = os.path.join(workdir, f'{save_name}.jpg')
    # 计算图片大小
    width = (fontsize - 1) * max(len(text) for text in text_list)
    height = (fontsize) * len(text_list) + 5

    # 创建一个空白图片，大小根据文字大小调整
    image = Image.new('RGB', (width, height), color=background)

    draw = ImageDraw.Draw(image)

    # 使用PIL的ImageFont创建字体对象
    font = ImageFont.truetype(font_path, fontsize)

    # 遍历列表中的每个元素，并将其绘制到图片上
    for i, text in enumerate(text_list):
        draw.text((0, i * fontsize), text, font=font, fill=color)
    image.save(workdir)
    # image.show()
    return image


def main(comment_item: dict, workdir, save_name):
    """
    :param comment_item: {用户名:评论}
    """
    comment_list = parse_comment_item(comment_item)
    text_to_image(comment_list, workdir, save_name)


if __name__ == '__main__':
    comment_item = {'123123': '好看好看', 'dsadasd': '太好看了'}
    main(comment_item, workdir=r'C:\Users\Administrator\Desktop', save_name='1')
