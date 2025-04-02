import sys
from pathlib import Path

# 添加项目根目录到PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import KIMI_API_KEY, KIMI_BASE_URL
from openai import OpenAI
import json

# 在文件顶部添加time模块导入
import time  # 新增耗时统计

def analyze_html_for_testing(html_file_path='page_content.html', ele_loc_file='eleLoc.json'):
    start_time = time.time()  # 新增开始时间记录
    client = OpenAI(
        api_key=KIMI_API_KEY,
        base_url=KIMI_BASE_URL,
    )

    try:
        file_object = client.files.create(file=Path(html_file_path), purpose="file-extract")
        file_content = client.files.content(file_id=file_object.id).text

        messages = [
            {
                "role": "system",
                "content": """你是一个资深自动化测试工程师，请根据网页内容生成规范的 JSON 数据：
                        1. 分析页面核心功能模块
                        2. 识别所有用户交互元素（页签切换按钮、各种点击按钮、输入框、链接等）及其用途，注意必须仅包含真实存在的交互元素
                        3. 为每个交互元素推荐最优定位方式，定位方式要保证唯一且稳定，推荐使用CSS选择器

                        输出要求：
                        - 使用规范的 JSON 格式
                        - 包含元素描述、定位策略
                        - 按模块进行分类组织

                        注意：仅输出 JSON 数据，无需任何其他解释或文字"""
            },
            {
                "role": "system",
                "content": file_content,
            },
            {"role": "user", "content": "根据我提供的 html 文件来分析我进行自动化测试需要的元素及其最优定位方式，定位方式必须唯一，例如‘菲尔斯特’等切换页签按钮、查询条件以及其他操作按钮等"},
        ]

        # 调用 chat-completion, 获取 Kimi 的回答
        completion = client.chat.completions.create(
            model="moonshot-v1-32k",
            messages=messages,
            temperature=0.3,
            max_tokens=2000  # 新增token限制
        )

        response_content = completion.choices[0].message.content

        try:
            # 解析 JSON 数据
            data = json.loads(response_content)
            # 将数据保存到指定文件名的文件
            with open(ele_loc_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已成功保存到 {ele_loc_file} 文件。")
            print(f"处理耗时: {time.time() - start_time:.2f}秒")  # 新增耗时输出
            return data
        except json.JSONDecodeError as e:
            # 新增错误处理：保存原始响应用于调试
            with open('raw_response.txt', 'w', encoding='utf-8') as f:
                f.write(response_content)
            print(f"原始响应已保存到 raw_response.txt，请检查以下问题：")
            print(f"1. 最后一个元素可能缺少闭合括号\n2. JSON 层级结构不完整\n3. 检查第130行附近的逗号分隔符")
            print(f"JSON 解析错误详情: {e}")
            print(f"处理耗时: {time.time() - start_time:.2f}秒")  # 新增耗时输出
            return None
    except FileNotFoundError:
        print(f"未找到文件: {html_file_path}")
        print(f"处理耗时: {time.time() - start_time:.2f}秒")  # 新增耗时输出
        return None


if __name__ == "__main__":
    # 可以在这里修改需要分析的 HTML 文件和保存文件名
    analyze_html_for_testing(html_file_path='sales_plan_body2_cleaned.html', ele_loc_file='sales_plan_location1.json')