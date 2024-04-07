# -*- coding: utf-8 -*-
def read(file_path):
    """
        读文件
    """
    f = open(file_path, "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    return ''.join(lines)

