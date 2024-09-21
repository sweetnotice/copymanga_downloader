import os
from PIL import Image, ImageDraw, ImageFont


def parse_comment_item(comment_item: dict) -> list:
    """
    :param comment_item: {用户名:评论}
    :return:
    """
    comment_list = []
    for user_name, send in comment_item.items():
        send = send.replace("，", ",")
        if len(send) <= 45:
            comment = f"{user_name} : {send}"
            comment_list.append(comment)
        elif 45 < len(send) <= 90:
            comment = f"{user_name} : {send[:45]}"
            comment_list.append(comment)
            comment = f"{send[45:]}"
            comment_list.append(comment)
    if len(comment_list) == 0:
        comment_list.append("暂无评论...")
    return comment_list


def create_text_image(text_list, font_size=16,
                      text_height_padding=2,
                      text_color=(0, 0, 0),
                      padding=10,
                      font_path='simhei.ttf'):
    """
    Parameters
    ----------
    text_list
    font_size
    text_height_padding :文本高度间隙
    text_color
    padding
    font_path

    Returns
    -------

    """
    # 设置字体
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # print("字体文件未找到，使用默认字体")
        font = ImageFont.load_default()

    # 计算图像尺寸
    max_width = 0
    total_height = 0
    for text in text_list:
        bbox = font.getbbox(text)  # 获取当前行的边界框
        text_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        if text_width > max_width:
            max_width = text_width
        total_height += line_height + text_height_padding

    image_width = max_width + 2 * padding  # 左右各加一些内边距
    image_height = total_height + 2 * padding  # 上下各加一些内边距

    # 创建空白图像
    img = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(img)

    # 绘制文本
    y = padding  # 起始y坐标
    for text in text_list:
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        x = padding
        draw.text((x, y), text, fill=text_color, font=font)
        y += (bbox[3] - bbox[1]) + text_height_padding  # 下一行

    return img


def main(comment_item: dict, workdir, save_name):
    """
    :param comment_item: {用户名:评论}
    """
    comment_list = parse_comment_item(comment_item)
    comment_img = create_text_image(comment_list)
    save_path = os.path.join(workdir, f"{save_name}.jpg")
    # comment_img.show()
    comment_img.save(save_path)


if __name__ == "__main__":
    comment_item = {
        "123123": "好看好看",
        "dsadasd": "太好看了",
        "我是用户": "dawoidjoawidjoiawjdoiawjdoija点击奥斯丁骄傲is大家哦爱设计的哦啊司机扫地就啊搜多久阿是降低阿斯",
    }
    comment_item = {
        "妮妮姆o": "剧情大概都能猜出来了（下一话）",
        "落叶": "剧情俗套（下一话）",
        "牧野神奈.": "盲猜黑长直是1",
        "坏事做尽屑粉毛": "真的好无聊（二刷）",
        "Fish/Bird": "诡计多端的姛，太老套了（下一话）",
        "fjwmlk": "有点无聊(下一话)",
        "1433223syyy": "切，多看一话都是浪费时间(下一话)",
        "看看上课": "好平庸的剧情（下一话）",
        "yitong111": "就这？（下一话）",
        "小小呼叫器": "就这样吧（下一话）",
        "ADJtttt": "不好看（下一话）",
        "与时光共存": "一般般(下一话)",
        "yasuo114514": "三刷了，还是这么没意思啊(下一章)",
        "aix的日记": "二刷(了，太没意思了(下一话)",
        "年年岁岁别经年": "无趣（下一章）",
        "虽是郃但真不以百合活": "典中典，真没劲头（二刷",
        "葉-": "就这啊（下一话）",
        "N.Chisato": "老套路（下一话）",
        "嘉隆JiaLong": "有点无聊（下一章）",
        "Niwanano": "白银御行：你缺不缺个书记当教练？",
        "yllskd": "放置上了哈哈，过两天估计就主动了",
        "Mostima._": "不好看(下一章)",
        "xtmmiao": "下一章",
        "drobo ly": "也就一般（下一章）",
        "神父竟是我自己": "她好会啊啊啊啊啊",
        "lljswl": "加载不出来可以用加速器",
        "291784138": "诡计多端的姛",
        "xllsjjz": "诡计多端的姛?",
        "3051768714": "我也不是什么白河豚（下一章）",
        "16536529224774": "哼！姛的欲情故纵罢了?【下一章】",
        "159****6402": "为什么我有的图片怎么都加载不出来啊……",
        "芝麻可以吃许墨嘛": "诡计多端的铜",
        "1245992b": "诡计多端的钕酮?",
        "afeiii": "诡计多端的钕铜?",
        "wkkk114514": "诡计多端的铜?",
        "ztjmar": "觉得还不够吗?",
        "Dianyindiao": "诡计多端",
        "无能鼠鼠": "还挺会拿捏分寸的",
        "Punk106": "露出鸡脚了吧",
        "超市偷鱼": "已经开始上钩了??",
        "192273809": "你干嘛～～～",
        "fuyuAme233": "诡计多端",
        "Lincoo": "拿捏的死死的",
        "鹿鸣幽涧": "定情信物（x",
        "Catdaren": "撩妹有一手呢",
        "搞姛被逮着了！": "先来刺激的试验底线，再循序渐进提升好感，拿捏女孩子有一手，高，实在是太高了",
    }
    main(comment_item, workdir=r"C:\Users\Arc\Desktop", save_name="1")
