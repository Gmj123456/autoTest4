import pandas as pd

# 读取原始文件
input_file = r"d:\gmj\workSpaces\workSpaces_pycharm\demo1\tag_4.3\tag.xlsx"
df = pd.read_excel(input_file)

# 取前100个标签
top_100_tags = df.head(100)

# 保存到新文件
output_file = r"d:\gmj\workSpaces\workSpaces_pycharm\demo1\tag_4.3\tag2.xlsx"
top_100_tags.to_excel(output_file, index=False)

print(f"成功提取前100个标签并保存到 {output_file}")