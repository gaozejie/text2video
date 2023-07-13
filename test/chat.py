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
                      data=json.dumps(body), headers=headers, stream=True)

    if r.status_code == 200:
        for chunk in r.iter_content(decode_unicode=True):
            # 处理响应的部分内容
            # 在这里添加你希望对响应进行的处理
            # 例如，将每个 chunk 解析为 JSON 数据

            # data = json.loads(chunk)
            # 处理数据...
            print(chunk)

    return  # 返回你需要的结果


if __name__ == '__main__':
    chatWithHuggingface("HuggingFaceH4/starchat-beta", "介绍一下什么时柯西不等式")
