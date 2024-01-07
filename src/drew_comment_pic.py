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
            comment = f'{user_name} : {send}'
            comment_list.append(comment)
        elif 45 < len(send) <= 90:
            comment = f'{user_name} : {send[:45]}'
            comment_list.append(comment)
            comment = f'{send[45:]}'
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
    # print(f'{workdir} 绘制完毕')
    # image.show()
    return image


def main(comment_item: dict, workdir, save_name):
    """
    :param comment_item: {用户名:评论}
    """
    comment_list = parse_comment_item(comment_item)
    text_to_image(comment_list, workdir, save_name)


if __name__ == '__main__':
    comment_item = {'123123': '好看好看', 'dsadasd': '太好看了',
                    '我是用户': 'dawoidjoawidjoiawjdoiawjdoija点击奥斯丁骄傲is大家哦爱设计的哦啊司机扫地就啊搜多久阿是降低阿斯'}
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
        "搞姛被逮着了！": "先来刺激的试验底线，再循序渐进提升好感，拿捏女孩子有一手，高，实在是太高了"
    }
    main(comment_item, workdir=r'C:\Users\Administrator\Desktop', save_name='1')
