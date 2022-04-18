#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :create_verify_img.py
# @Time      :10/26/21 5:48 PM
# @Author    :Zhidong R

import os
import random
from io import BytesIO
# captcha是用于生成验证码图片的库，可以 pip install captcha 来安装它
from captcha.image import ImageCaptcha


def random_captcha_text(num):
    # 验证码列表
    captcha_text = []
    for i in range(10):  # 0-9数字
        captcha_text.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        captcha_text.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        captcha_text.append(chr(i))

    # 从list中随机获取6个元素，作为一个片断返回
    example = random.sample(captcha_text, num)

    # 将列表里的片段变为字符串并返回
    verification_code = ''.join(example)
    return verification_code

# 生成字符对应的验证码
def generate_captcha_image(verify_code:str , path = None):
    # # 获得随机生成的验证码
    # captcha_text = random_captcha_text(4)
    # # 把验证码列表转为字符串
    # captcha_text = ''.join(captcha_text)
    # # 生成验证码
    captcha_text = verify_code
    image = ImageCaptcha()

    if path:
        if not os.path.exists(path):
            os.makedirs(path)
        img_path = os.path.join(path, captcha_text + '.png')
        image.write(output=img_path)

    out = BytesIO()
    image.write(captcha_text, output=out, format='jpeg')
    return out

def create_verify_code_and_img(num=4):
    """
    生成验证码和图片
    :param num: 验证码的位数，默认四位
    :return: 元组，格式（验证码字符串，图片路径）
    """
    verify_code = random_captcha_text(num)
    image = generate_captcha_image(verify_code)

    return verify_code, image


if __name__ == '__main__':
    pass
    # number = 1000
    # for i in range(number):
    #     generate_captcha_image()
    # print(create_verify_code_and_img())
