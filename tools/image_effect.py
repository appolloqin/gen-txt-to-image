# -*- coding: utf-8 -*-
from PIL import Image, ImageSequence, ImageEnhance


def add_fade_effect(image_path, duration=1):
    """
    给图片添加淡入淡出动画效果。
    :param image_path: 图片文件路径。
    :param duration: 每帧持续时间（秒）。
    """
    image = Image.open(image_path)
    width, height = image.size

    # 生成淡入淡出的渐变掩码
    def fade_mask(t):
        return int(255 * (1 - min(1, t / (duration / 2))))

    frames = []
    for i in range(int(duration * 60) // 2):  # 每秒60帧
        # 生成淡入渐变
        fade_in = Image.new('RGBA', (width, height), (0, 0, 0, fade_mask(i)))
        frames.append(Image.composite(Image.blend, image, fade_in))

        # 生成淡出渐变
        fade_out = Image.new('RGBA', (width, height), (0, 0, 0, 255 - fade_mask(i + duration * 60 // 2)))
        frames.append(Image.composite(Image.blend, image, fade_out))

    # 保存为GIF动画
    frames[0].save('fade_effect.gif', save_all=True, append_images=frames[1:], duration=duration, loop=0)


# 使用例子
add_fade_effect('1.png', duration=1)  # 图片路径，持续时间为1秒的淡入淡出动画