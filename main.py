# -*- coding: utf-8 -*-
import erniebot
from tools.config_tool import get_conf
from tools.read_file import read
from tools.stable_api import txt2img
from tools.generate_video import image_to_video_mp4


def str_to_jsonstr(data: str):
    """
    过滤字符串
    :param data:
    :return:
    """
    start_index = data.find("```json")
    end_index = data.rfind("```")
    del_json = data[start_index+8:end_index]
    return del_json


def main():
    print('------------------文章生成图片提示词-------------------')
    API_TYPE, ACCESS_TOKEN, WEB_PORT, LLM_MODEL = get_conf('API_TYPE', 'ACCESS_TOKEN', 'WEB_PORT', 'LLM_MODEL')
    erniebot.api_type = API_TYPE
    erniebot.access_token = ACCESS_TOKEN
    prefix_prompt = "你是一个提示词专家，你的任务是辅助我生成优质的文生图提示词，要求：1.文章按照句号分隔；2.每句话生成一个文生图提示词；3.输出json格式数据，内容标签content,提示词标签prompt。内容如下："
    content = read('F:/WorkSpace/Python/ChatGPT/gen-txt-to-image/content.txt')
    stream = False
    response = erniebot.ChatCompletion.create(
        # model=LLM_MODEL,
        model='ernie-4.0',
        messages=[{'role': 'user', 'content': prefix_prompt + content}],
        stream=stream)

    result = ""
    if stream:
        for resp in response:
            result += resp.get_result()
    else:
        result = response.get_result()
    print(result)
    dict_data = eval(str_to_jsonstr(result))
    print('------------------文生图片-------------------')
    i = 1
    for prompt_item in dict_data:
        txt2img(prompt=prompt_item['prompt'], image_name=str(i)+'.png')
        i = i+1
        print('第'+str(i)+'张图')
    print('------------------生成视频开始-------------------')
    image_to_video_mp4(output='threeyear.mp4',height=768,width=1024)
    print('------------------生成视频成功-------------------')


if __name__ == "__main__":
    main()
