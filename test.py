from PIL import Image, ImageDraw, ImageFont
import textwrap


def create_image(comments, font_path='C:/Windows/Fonts/simsun.ttc'):
    # 设置字体和字体大小
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    # 计算每行的最大宽度和总高度
    max_width = 0
    total_height = 0
    line_height = font.getsize('国')[1]
    lines = []
    for comment in comments:
        # 自动换行
        comment_lines = textwrap.wrap(comment, width=30)
        lines += comment_lines
        line_width, line_height = font.getsize(comment_lines[0])
        max_width = max(max_width, line_width)
        total_height += line_height * len(comment_lines)

    # 创建一个新的图片对象
    image = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 将评论画到图像上
    y_text = 0
    for line in lines:
        draw.text((0, y_text), line, font=font, fill=(0, 0, 0))
        y_text += line_height

    # 保存图像
    image.save('comments.png')


comments = ['这是一个关于漫画的评论', '这又是一个关于漫画的评论', '这还是一个关于漫画的评论']
create_image(comments)