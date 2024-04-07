# -*- coding: utf-8 -*-
import cv2 as cv
from PIL import Image
import numpy as np
import os
import math
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_img = project_dir+'/output/image/'
path_video = project_dir+'/output/video/'
path_video_avi = project_dir+'/output/video/test.avi'
video_name = 'test.mp4'


def image_to_video_mp4(file_path=path_img, output=video_name, height=512, width=512, fps=60,effects=True):
    print('file_path:'+file_path)
    # 生成图片目录下以图片名字为内容的列表
    img_list = os.listdir(file_path)
    # 用于mp4格式的生成
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    # 创建一个写入视频对象
    videowriter = cv.VideoWriter(path_video+output, fourcc, fps, (width, height))
    for img in img_list:
        path = file_path + img
        if len(img) < 4:
            continue
        if effects:
            # for i in range(181):
            for i in range(fps + 1):
                # print(i)
                # frame = cv.imread(path)
                frame = pillow_to_cv(image_crop(path, height, width, i))
                # 特效
                if i > 52:
                    if i % 2 == 0:#光照
                      frame = illumination_image(frame)
                    else:#流年
                      frame = flow_image(frame)
                videowriter.write(frame)
        else:
            frame = cv.imread(path)
            for i in range(fps+1):
                videowriter.write(frame)

        # frame = cv.imread(path)
        # videowriter.write(frame)
    videowriter.release()


def image_resize(image_path, height, width):
    image = Image.open(image_path)
    new_size = (width, height)
    return image.resize(new_size)


def image_crop(image_path, height, width, step):
    image = Image.open(image_path)
    height_n = image.height
    width_n = image.width
    s_height = height_n/800
    s_width = width_n/800
    new_size = (s_width*step, s_height*step, width_n-s_width*step, height_n-s_height*step)
    crop_image = image.crop(new_size)
    return crop_image.resize((width, height))


def pillow_to_cv(image_pil):
    return cv.cvtColor(np.asarray(image_pil),cv.COLOR_RGB2BGR)


def cv_to_pillow(image_cv):
    return Image.fromarray(cv.cvtColor(image_cv,cv.COLOR_BGR2RGB))


def image_to_video_avi(file_path=path_img, output=path_video_avi, height=512, width=512, fps=60):
    # 生成图片目录下以图片名字为内容的列表
    img_list = os.listdir(file_path)
    # avi格式的生成
    fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # 创建一个写入视频对象
    videowriter = cv.VideoWriter(output, fourcc, fps, (width, height))
    for img in img_list:
        path = file_path + img
        # print(path)
        if len(img) < 4:
            continue
        for i in range(501):
            # frame = cv.imread(path)
            frame = pillow_to_cv(image_crop(path,height,width,i))
            videowriter.write(frame)
        # frame = cv.imread(path)
        # videowriter.write(frame)
    videowriter.release()

def illumination_image(img):
    """
    光照特效 img = cv.imread
    :return:
    """
    # 获取图像行和列
    rows, cols = img.shape[:2]
    # 设置中心点和光照半径
    centerX = rows / 2 - 20
    centerY = cols / 2 + 20
    radius = min(centerX, centerY)
    # 设置光照强度
    strength = 100
    # 新建目标图像
    dst = np.zeros((rows, cols, 3), dtype="uint8")
    # 图像光照特效
    for i in range(rows):
        for j in range(cols):
            # 计算当前点到光照中心距离(平面坐标系中两点之间的距离)
            distance = math.pow((centerY - j), 2) + math.pow((centerX - i), 2)
            # 获取原始图像
            B = img[i, j][0]
            G = img[i, j][1]
            R = img[i, j][2]
            if (distance < radius * radius):
                # 按照距离大小计算增强的光照值
                result = (int)(strength * (1.0 - math.sqrt(distance) / radius))
                B = img[i, j][0] + result
                G = img[i, j][1] + result
                R = img[i, j][2] + result
                # 判断边界 防止越界
                B = min(255, max(0, B))
                G = min(255, max(0, G))
                R = min(255, max(0, R))
                dst[i, j] = np.uint8((B, G, R))
            else:
                dst[i, j] = np.uint8((B, G, R))

    return dst


def flow_image(img):
    """
    流年特效
    :param img: img = cv.imread
    :return:
    """
    # 获取图像行和列
    rows, cols = img.shape[:2]
    # 新建目标图像
    dst = np.zeros((rows, cols, 3), dtype="uint8")
    # 图像流年特效
    for i in range(rows):
        for j in range(cols):
            # B通道的数值开平方乘以参数12
            B = math.sqrt(img[i, j][0]) * 12
            G = img[i, j][1]
            R = img[i, j][2]
            if B > 255:
                B = 255
            dst[i, j] = np.uint8((B, G, R))
    return dst


def filter_image(img):
    """
    图像滤镜
    :param img: img = cv.imread
    :return:
    """
    # 获取滤镜颜色
    def getBGR(image_bgr, table, i, j):
        # 获取图像颜色
        b, g, r = image_bgr[i][j]
        # 计算标准颜色表中颜色的位置坐标
        x = int(g / 4 + int(b / 32) * 63)
        y = int(r / 4 + int((b % 32) / 4) * 63)
        # 返回滤镜颜色表中对应的颜色
        return lj_map[x][y]
    # 滤镜图像
    lj_map = img
    # 获取图像行和列
    rows, cols = img.shape[:2]
    # 新建目标图像
    dst = np.zeros((rows, cols, 3), dtype="uint8")
    # 循环设置滤镜颜色
    for i in range(rows):
        for j in range(cols):
            dst[i][j] = getBGR(img, lj_map, i, j)
    return dst


def nostalgia_image(img):
   """
   :param img:
   :return:
   """
   # 获取图像行和列
   rows, cols = img.shape[:2]
   # 新建目标图像
   dst = np.zeros((rows, cols, 3), dtype="uint8")
   # 图像怀旧特效
   for i in range(rows):
       for j in range(cols):
           B = 0.272 * img[i, j][2] + 0.534 * img[i, j][1] + 0.131 * img[i, j][0]
           G = 0.349 * img[i, j][2] + 0.686 * img[i, j][1] + 0.168 * img[i, j][0]
           R = 0.393 * img[i, j][2] + 0.769 * img[i, j][1] + 0.189 * img[i, j][0]
           if B > 255:
               B = 255
           if G > 255:
               G = 255
           if R > 255:
               R = 255
           dst[i, j] = np.uint8((B, G, R))

   return dst


def sketch_image(img):
     """
     素描特效
     :param img:
     :return:
     """
     # 图像灰度处理
     gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
     # 高斯滤波降噪
     gaussian = cv.GaussianBlur(gray, (5, 5), 0)
     # Canny算子
     canny = cv.Canny(gaussian, 50, 150)
     # 阈值化处理
     ret, result = cv.threshold(canny, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
     return result
