# 在文件顶部添加必要的导入
import time  # 新增时间模块
import json
import requests
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import GUIJI_API_KEY, GUIJI_BASE_URL

# 将现有代码封装到函数中
def analyze_html_elements(html_file_path, ele_loc_file):
    start_time = time.time()  # 记录开始时间
    
    try:
        with open(html_file_path, "rb") as f:
            files = {
                "file": ("sales_plan.html", f, "text/html"), 
                "purpose": (None, "batch") 
            }

            url = GUIJI_BASE_URL
            
            headers = {
                # "Authorization": "Bearer GUIJI_API_KEY",
                "Authorization": f"Bearer {GUIJI_API_KEY}",
                "Content-Type": "application/json"  # 修改为JSON格式
            }
            
            # 将HTML内容作为消息内容发送（修复变量名）
            with open(html_file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            payload = {
                "model": "deepseek-ai/DeepSeek-V3",
                "messages": [
                    {
                        "role": "system",
                        "content": """你是一个JSON生成器，请严格按以下要求输出：
                        1. 必须输出纯净的JSON格式
                        2. 最外层用花括号包裹
                        3. 禁止包含```json代码块标记
                        4. 所有字符串使用双引号
                        5. 确保没有尾随逗号"""
                         + 
                        """ 1. 分析页面核心功能模块
                        2. 识别所有用户交互元素（如页签切换按钮、各种点击按钮、输入框、链接等）及其用途，注意必须仅包含真实存在的交互元素
                        3. 为每个交互元素推荐最优定位方式，定位方式要保证唯一且稳定，尽量使用CSS选择器"""
                    },
                    {
                        "role": "system",
                        "content": html_content  
                    },
                    {"role": "user", "content": "根据我提供的 html 文件来分析我进行自动化测试需要的元素及其最优定位方式"},
            ]
            }
            
            # 发送POST请求（新增关键调用）
            response = requests.post(url, headers=headers, json=payload)
            
            # 增强响应处理
            try:
                response_data = response.json()
                if response.status_code != 200:
                    print(f"API异常响应: {response.text}")
                    return None
                
                # 强化内容清洗
                response_content = response_data["choices"][0]["message"]["content"].strip()
                response_content = response_content.replace('```json', '').replace('```', '')
                response_content = response_content.split('{', 1)[-1].rsplit('}', 1)[0]  # 提取花括号间内容
                response_content = '{' + response_content + '}'  # 重新包裹为合法JSON

                # 立即验证并保存原始响应
                with open('raw_response.txt', 'w', encoding='utf-8') as f:
                    f.write(response_content)
                
                data = json.loads(response_content)
                # 将数据保存到指定文件名的文件
                with open(ele_loc_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"数据已成功保存到 {ele_loc_file} 文件。")
                print(f"处理耗时: {time.time() - start_time:.2f}秒")  # 新增耗时统计
                return data
            except json.JSONDecodeError as e:
                # 新增错误处理：保存原始响应用于调试
                with open('raw_response.txt', 'w', encoding='utf-8') as f:
                    f.write(response_content)
                print(f"原始响应已保存到 raw_response.txt，请检查以下问题：")
                print(f"1. 最后一个元素可能缺少闭合括号\n2. JSON 层级结构不完整\n3. 检查第130行附近的逗号分隔符")
                print(f"JSON 解析错误详情: {e}")
                print(f"处理耗时: {time.time() - start_time:.2f}秒")  # 新增耗时统计
                return None
    except FileNotFoundError:
        print(f"未找到文件: {html_file_path}")
        print(f"处理耗时: {time.time() - start_time:.2f}秒")  # 新增耗时统计
        return None

# 在文件底部添加主程序入口
if __name__ == "__main__":
    html_path = r"./sales_plan_body2_cleaned.html"
    output_path = "element_locations_guijiliudong.json"  # 定义输出文件路径
    analyze_html_elements(html_path, output_path)

