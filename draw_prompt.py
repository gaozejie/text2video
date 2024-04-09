from openai import OpenAI
import os
from dotenv import load_dotenv
import json


def generate_prompt(user_input):
    # 尝试加载环境变量文件
    load_dotenv('.env', override=True)
    # 尝试加载本地开发环境变量文件
    load_dotenv('.local.env', override=True)

    MIDJOURNEY_PROMPT = '''你好，你是一个可以生成 midjourney 提示词的专家，用户给你一段描述，你来生成对应的提示词!

    请你记住，你要生成的提示词是英文的 ，其格式可能类似于：

    As the sun gently kissed the horizon, casting a warm golden glow across the bustling city streets, a captivating sight unfolded before my eyes. A graceful woman, adorned in an elegant dress that fluttered in the gentle breeze, held a porcelain cup of steaming coffee in her delicate hands.

    ，不要解释用户的任何输入，不需要任何其他废话，我希望你输出的格式是 Json,如下：

    {
    "result":"$prompt"
    }
    '''

    # 读取环境变量
    api_key = os.getenv('OPEN_AI_API_KEY')
    base_url = os.getenv('OPEN_AI_BASE_URL')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-32k", # 这个模型基本够用了
            messages=[
                {"role": "system", "content": MIDJOURNEY_PROMPT},
                {"role": "user", "content": user_input},
            ],
            temperature=0.3,
        )
    except Exception as e:
        raise RuntimeError("Failed to create completion: " + str(e))

    try:
        content = json.loads(completion.choices[0].message.content)
        return content['result']
    except (IndexError, KeyError, json.JSONDecodeError):
        raise RuntimeError("Failed to parse completion result")


if __name__ == '__main__':
    user_input = '''你是谁'''
    print(generate_prompt(user_input))  # As humanity took its first steps on the lunar surface, the vast expanse of the moon's barren landscape stretched out before them, illuminated by the distant glow of Earth. The momentous occasion marked a triumph of human ingenuity and perseverance, forever changing our understanding of the cosmos and our place within it.
