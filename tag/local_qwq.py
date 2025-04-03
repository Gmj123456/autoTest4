"""

"""
import pandas as pd
import requests
import json
import time
import datetime

# API端点
url = "http://192.168.150.108:11434/api/generate"

def classify_tag(tag):
    """对单个标签进行分类"""
    payload = {
        "model": "qwq",
        # "model": "deepseek-r1:32b",
        "prompt": f'''你是一位拥有20年专业经验的TikTok全球运营专家，精通跨文化社交媒体策略与多语言内容优化，擅长通过语义分析与文化适配实现精准标签分类。
                    分类原则：
                        严格一对一映射：每个标签仅属于1个类目，若存在模糊性，按以下优先级决策：
                        a) 业务场景匹配度（如#OOTD优先归入#穿搭类而非#日常）
                        b) 语义强关联性（如#BookTok归入#文化而非#教育）
                        c) 平台热门类目趋势
                    
                    英文标签处理：
                        执行语义分词（如#SustainableFashion拆分为"可持续+时尚"）
                        翻译需符合中文表达习惯（如#POV不直译为"观点"，按平台惯例译作"第一视角"）

                    输出要求：
                        - 仅返回分类结果，不要返回思考过程
                    输出格式：
                        原始标签 (Original), 中文翻译 (Translation), 所属类目 (Category), 置信度 (Confidence)
                        #OOTD, 每日穿搭, 时尚潮流, 98%
                        #POV, 第一视角, 内容形式, 92%
                    
                    强制性校验：
                        输入/输出标签数量绝对一致    
                        输出标签必须100%来源于输入列表
                        禁止任何形式的标签改写或补充
                    
                    异常处理：
                        若遇文化特殊标签（如#Diwali），需结合节日属性而非直译（归入#节日庆典而非#文化）
                        多义词标签以当前平台主流用法为准（如#Apple默认指品牌而非水果）
                    
                    请对以下标签进行分类：{tag}''',
        "max_tokens": 100000,
        "stream": False,
        "top_p": 1,
        "options": {
            "num_ctx": 20000
        }
    }

    max_retries = 3
    retry_delay = 5  # 重试间隔时间（秒）

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=2000)  # 超时时间
            if response.status_code == 200:
                return response.json()['response']
            else:
                print(f"标签 {tag} 分类失败，状态码：{response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"标签 {tag} 分类出错，正在重试 ({attempt + 1}/{max_retries})：{e}")
                time.sleep(retry_delay)
            else:
                print(f"标签 {tag} 分类最终失败：{e}")
                return None


def process_tags_from_excel(file_path):
    """从Excel或txt文件中读取标签并进行分类"""
    try:
        # 根据文件扩展名选择读取方式
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                tags = [line.strip() for line in f if line.strip()]
            df = pd.DataFrame(tags, columns=['tag_name'])
        else:
            raise ValueError("仅支持.xlsx和.txt文件格式")

        # 确保表头是tag_name
        if 'tag_name' not in df.columns:
            raise ValueError("文件必须包含'tag_name'列或标签数据")

        # 创建结果文件，加入时间戳
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = file_path.replace('.xlsx', f'_result_qwq_{timestamp}.csv').replace('.txt', f'_result_qwq_{timestamp}.csv')
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write("tag_name,category\n")

        # 处理每个标签
        for index, row in df.iterrows():
            tag = row['tag_name']
            if pd.isna(tag) or not tag.strip():
                continue

            start_time = time.time()
            print(f"正在处理标签: {tag}")

            # 调用模型进行分类
            category = classify_tag(tag)

            if category:
                # 去掉思考过程，只保留最终分类结果
                category = category.split('\n')[-1].strip()
                print(f"分类结果: {category}")
                # 将结果写入文件
                with open(result_file, 'a', encoding='utf-8') as f:
                    f.write(f"{tag},{category}\n")
            else:
                print("分类失败")

            print(f"处理耗时: {time.time() - start_time:.2f}秒\n")

    except Exception as e:
        print(f"处理Excel文件时出错: {str(e)}")


if __name__ == "__main__":
    # Excel文件路径
    excel_path = r"d:\gmj\workSpaces\workSpaces_pycharm\demo1\tag_4.3\test_tag_original.txt"

    # 处理标签
    process_tags_from_excel(excel_path)