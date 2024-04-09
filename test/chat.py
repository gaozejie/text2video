import requests
import json
import os
from dotenv import load_dotenv
load_dotenv('.env', override=True)

# 尝试加载本地开发环境变量文件
load_dotenv('.local.env', override=True)

# 获取当前脚本所在的目录
current_directory = os.getcwd()

# 读取环境变量
api_token = os.getenv('API_TOKEN')

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}


def chatWithHuggingface(model, prompt):
    body = {
        "inputs": prompt
    }
    r = requests.post("https://api-inference.huggingface.co/models/" + model,
                      data=json.dumps(body), headers=headers,)

    if r.status_code == 200:
        print(r.json())
    else:
        print(r.status_code)
        print(r.text)


if __name__ == '__main__':
    # chatWithHuggingface("HuggingFaceH4/starchat-beta", "介绍一下什么时柯西不等式")
    chatWithHuggingface("ByteDance/SDXL-Lightning", "As humanity took its first steps on the lunar surface, the vast expanse of the moon's barren landscape stretched out before them, illuminated by the distant glow of Earth. The momentous occasion marked a triumph of human ingenuity and perseverance, forever changing our understanding of the cosmos and our place within it.")
