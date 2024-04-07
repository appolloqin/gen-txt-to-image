# gen-txt-to-image
一款文生视频应用，用于小说推文，生成漫画等视频。使用主流大模型，结合Stable Diffusion，实现文生图，图生视频本地化私有部署。
# 1.安装python3.10环境
conda create -n image python=3.10 或者其他方式安装（conda安装请自行搜索安装）
# 2.安装依赖包
pip install -r requirements.txt
# 3.安装成功后，运行项目
项目根目录下windows  dos进入项目根目录。执行命令python main.py
# 成果展示 
[视频](https://github.com/appolloqin/gen-txt-to-image/output/video/threeyear.mp4)
# 说明
执行成功后会在output/image下生成图片。
会在output/video下生成视频。
# 其他说明
使用文心一言，生成prompt，使用stable diffusion生成图片，使用opencv合成视频。<br>
其他大模型需要自定义开发。需要申请文心一言token,申请地址[地址](https://aistudio.baidu.com/index/accessToken)<br>
需要在本地部署stable diffusion webui [地址](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 端口7860
