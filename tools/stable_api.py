# -*- coding: utf-8 -*-
# api文档 http://127.0.0.1:7860/docs
# 第三方api调用库 https://github.com/mix1009/sdwebuiapi
import requests
import base64
import os
# Define the URL and the payload to send.
url = "http://127.0.0.1:7860"
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_img = project_dir+'/output/image/'
path_image = project_dir+'/output/locimg/'


def txt2img(prompt='puppy dog',image_name='test.png'):
    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 1024,
        "height": 768,
        "sampler_index": "Euler a",
        "override_settings": {
        "sd_model_checkpoint": "novelV1"}
    }
    # Send said payload to said URL through the API.
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    print('--------')
    print(response)
    r = response.json()
    # Decode and save the image.
    check_and_create_path(path_img)
    with open(path_img+image_name, 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))


def txt2img_imgname(prompt='puppy dog', negative_prompt='', sampler='DPM++ 3M SDE Karras', image_name='test.png', img_path='1/'):
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": 35,
        "width": 1024,
        "height": 768,
        "sampler_index": sampler,
        "override_settings": {
        "sd_model_checkpoint": "tianyuan"}
    }
    # Send said payload to said URL through the API.
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    print('--------')
    print(response)
    r = response.json()
    # Decode and save the image.
    check_and_create_path(path_image+img_path)
    with open(path_image+img_path+image_name, 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))


def check_and_create_path(path):
    # 检查路径是否存在
    if not os.path.exists(path):
        # 如果路径不存在，则创建
        try:
            os.makedirs(path)
        except OSError as e:
            # 如果创建过程中出现错误（例如目录已存在），则打印错误信息并跳过
            print(f"Error: {e}")
    else:
        print(f"Path '{path}' exists.")

