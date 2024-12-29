import requests
import os

# 下载图片
def Download(name,url):
    r = requests.get(url)
    folder_path = ""  # 指定文件夹路径
    file_name = name  # 文件名

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)  # 构建完整的文件路径
    with open(file_path, "wb") as f:
        f.write(r.content)
