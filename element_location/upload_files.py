from pathlib import Path
from openai import OpenAI
import json
import re

def analyze_html_for_testing():
    client = OpenAI(
        api_key="sk-Mm6vK2FK3bk08Spuu4DcB0roLyAbeepsaq2lcPgf1fip8qk7",
        base_url="https://api.moonshot.cn/v1",
    )

    file_object = client.files.create(file=Path("page_content.html"), purpose="file-extract")

    file_content = client.files.content(file_id=file_object.id).text

    # 把它放进请求中
    messages = [
        {
            "role": "system",
            "content": """你是一个资深自动化测试工程师，请根据网页内容生成规范的 JSON 数据：
                    1. 分析页面核心功能模块
                    2. 识别所有用户交互元素（如按钮、输入框、链接等）及其用途
                    3. 为每个交互元素推荐最优定位方式（按优先级排列），定位方式要保证唯一且稳定
                    4. 说明推荐理由

                    输出要求：
                    - 使用规范的 JSON 格式
                    - 包含元素描述、定位策略、优先级和理由
                    - 按模块进行分类组织

                    注意：仅输出 JSON 数据，无需任何其他解释或文字"""
        },
        {
            "role": "system",
            "content": file_content,
        },
        {"role": "user", "content": "根据我提供的 html 文件来分析我进行自动化测试需要的元素及其最优定位方式"},
    ]

    # 然后调用 chat-completion, 获取 Kimi 的回答
    completion = client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=messages,
        temperature=0.3,
    )

    response_content = completion.choices[0].message.content

    try:
        # 解析 JSON 数据
        data = json.loads(response_content)
        # 将数据保存到 output.json 文件
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("数据已成功保存到 output.json 文件。")
        return data
    except json.JSONDecodeError as e:
        print(f"提取到的 content 内容：\n{response_content}")
        print(f"JSON 解析错误: {e}")
        return None


if __name__ == "__main__":
    analyze_html_for_testing()