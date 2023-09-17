import os
from PIL import Image, ImageDraw, ImageFont


def parse_comment_item(comment_item: dict) -> list:
    """
    :param comment_item: {用户名:评论}
    :return:
    """
    comment_list = []
    for k, v in comment_item.items():
        comment = f'{k} : {v}'
        comment_list.append(comment)
    return comment_list


def drew_comment(comment_list: list, workdir, name):
    workdir = os.path.join(workdir, name)
    # 加载图片
    img = Image.new("RGB", (800, 1000), (255, 255, 255))
    # 设置字体
    font = ImageFont.truetype("msyh.ttc", 19)
    # 创建绘图对象
    draw = ImageDraw.Draw(img)
    # 设置开始坐标
    y = 0
    # 循环绘制每个评论
    for comment in comment_list:
        draw.text((0, y), comment, fill=(0, 0, 0), font=font)
        y += 20
        # 保存图片
    img.save(f'{workdir}.jpg')
    print(f'{workdir}  评论页绘制完毕\n', end='')


def main(comment_item: dict, workdir, save_name):
    comment_list = parse_comment_item(comment_item)
    drew_comment(comment_list, workdir, save_name)


if __name__ == '__main__':
    pass
