from openai import OpenAI
import pandas as pd
import datetime
import time
import os

client = OpenAI(api_key="sk-b39e67efb7094093b5d0736ae91cdc3c", base_url="https://api.deepseek.com")

def process_tags_from_file(file_path):
    """从Excel或txt文件中读取标签并进行分类"""
    try:
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

        # 初始化统计变量
        total_time = 0
        total_tokens = 0
        tag_count = 0
        results = []  # 用于存储每个标签的详细结果

        # 处理每个标签
        for index, row in df.iterrows():
            tag = row['tag_name']
            if pd.isna(tag) or not tag.strip():
                continue

            print(f"正在处理标签: {tag}")
            
            # 记录开始时间
            start_time = time.time()

            # 调用模型分类标签
            """----------------------------------------------"""

            model = "deepseek-chat"  # V3
            # model="deepseek-reasoner"  # R1
            response = client.chat.completions.create(
            model=model,  # 使用变量
            messages=[
                {"role": "system", 
                "content": """
                你是一位拥有20年专业经验的TikTok全球运营专家，精通跨文化社交媒体策略与多语言内容优化，擅长通过语义分析与文化适配实现精准标签分类。
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
                
                """},
                {"role": "user", "content": f"请对以下标签进行分类：{tag}"},
            ],
            stream=False
        )

            """----------------------------------------------"""

            # 处理分类结果
            result = response.choices[0].message.content
            if result:
                # 解析结果
                result_parts = result.split(',')
                if len(result_parts) >= 4:
                    original, translation, category, confidence = result_parts[:4]
                    # 去除标签名中的井号
                    original = original.lstrip('#')
                else:
                    original, translation, category, confidence = tag, '', '', ''
                    # 去除标签名中的井号
                    original = original.lstrip('#')

                # 计算耗时和token
                end_time = time.time()
                elapsed_time = end_time - start_time
                tokens_used = response.usage.total_tokens
                
                # 更新统计
                total_time += elapsed_time
                total_tokens += tokens_used
                tag_count += 1

                # 存储结果
                results.append({
                    '标签名': original.strip(),
                    '翻译': translation.strip(),
                    '类目名': category.strip(),
                    '置信度': confidence.strip(),
                    '处理时间': elapsed_time,
                    '使用token': tokens_used
                })

                print(f"分类结果: {result}")
                print(f"处理时间: {elapsed_time:.2f}秒, 使用token: {tokens_used}\n")

        # 创建统计信息DataFrame
        stats_df = pd.DataFrame(results)
        
        # 添加序号列
        stats_df.insert(0, '序号', range(1, len(stats_df) + 1))
        
        # 添加统计信息
        stats_df.loc['总计'] = {
            '序号': '总计',
            '标签名': '',
            '翻译': '',
            '类目名': '',
            '置信度': '',
            '处理时间': total_time,
            '使用token': total_tokens
        }
        
        stats_df.loc['平均值'] = {
            '序号': '平均值',
            '标签名': '',
            '翻译': '',
            '类目名': '',
            '置信度': '',
            '处理时间': total_time/tag_count,
            '使用token': total_tokens/tag_count
        }

        # 创建输出文件夹：detailed_output描述详细信息和result仅输出结果
        detailed_output_dir = os.path.join(os.path.dirname(file_path), 'detailed_output')
        result_dir = os.path.join(os.path.dirname(file_path), 'result')
        os.makedirs(detailed_output_dir, exist_ok=True)
        os.makedirs(result_dir, exist_ok=True)

        # 创建时间戳
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # 保存统计信息到Excel
        model_name = model  # 使用API调用时的模型名称
        detailed_file = os.path.join(detailed_output_dir, os.path.basename(file_path).replace('.xlsx', f'_{model_name}_detailed_{timestamp}.xlsx').replace('.txt', f'_{model_name}_detailed_{timestamp}.xlsx'))
        stats_df.to_excel(detailed_file, index=False)

        # 保存简单结果到Excel
        simple_df = pd.DataFrame([{'标签名': r['标签名'], '翻译': r['翻译'], '类目名': r['类目名']} for r in results])
        simple_file = os.path.join(result_dir, os.path.basename(file_path).replace('.xlsx', f'_{model_name}_simple_{timestamp}.xlsx').replace('.txt', f'_{model_name}_simple_{timestamp}.xlsx'))
        simple_df.to_excel(simple_file, index=False)

        # 输出统计信息
        if tag_count > 0:
            avg_time = total_time / tag_count
            avg_tokens = total_tokens / tag_count
            print(f"\n统计信息:")
            print(f"总标签数: {tag_count}")
            print(f"总处理时间: {total_time:.2f}秒")
            print(f"总使用token: {total_tokens}")
            print(f"平均处理时间: {avg_time:.2f}秒/标签")
            print(f"平均使用token: {avg_tokens:.1f}/标签")

    except Exception as e:
        print(f"处理文件时出错: {str(e)}")

if __name__ == "__main__":
    # 文件路径
    file_path = r"d:\gmj\workSpaces\workSpaces_pycharm\demo1\tag_4.3\tag.xlsx"  # 或.xlsx文件
    # file_path = r"d:\gmj\workSpaces\workSpaces_pycharm\demo1\tag_4.3\test_tag_original.txt"  # 或.xlsx文件

    # 处理标签
    process_tags_from_file(file_path)