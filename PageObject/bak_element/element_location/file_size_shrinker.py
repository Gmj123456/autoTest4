"""
    精简策略：
    0.只保留class = "main"和class="ant-tabs-nav-scroll"的div；
    1. 移除侧边导航栏、顶部栏，只保留主要内容区域；（侧边栏部分有很多菜单项，可能包含多个链接和子菜单。顶部栏有用户信息、通知、设置等元素。）
    2. 移除不必要的 JavaScript 代码；
    3. 移除内联样式代码；
    4. 移除SVG图标、移除img标签；
    5. 移除不必要的 CSS 代码：删除所有的 <style> 标签及其内容；
    6. 移除不必要的 HTML 注释：删除所有的 HTML 注释。
    7. 移除不必要的空格和换行符：删除所有的空格和换行符，包括标签之间的空格。
"""

from bs4 import BeautifulSoup
from bs4.element import Comment

def remove_unnecessary_content(html_content):
    """
    移除 HTML 内容中的不必要部分，包括侧边栏、顶部栏、JavaScript、内联样式、SVG、CSS、HTML注释和空格换行符
    返回清理后的 HTML 字符串
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # +++ 新增策略0：只保留class="main"的div +++
    # +++ 策略0：保留main和ant-tabs-nav-scroll的div +++
    preserved_divs = []
    # 查找两个目标div
    main_div = soup.find('div', class_='main')
    tabs_div = soup.find('div', class_='ant-tabs-nav-scroll')
    
    if main_div:
        preserved_divs.append(main_div)
    if tabs_div:
        preserved_divs.append(tabs_div)
    
    if preserved_divs:
        # 创建包含保留元素的容器
        new_soup = BeautifulSoup('<div id="preserved-container"></div>', 'html.parser')
        container = new_soup.find('div', id='preserved-container')
        for div in preserved_divs:
            container.append(div)
        soup = new_soup
    if main_div:
        # 创建新soup对象仅包含主内容区域
        soup = BeautifulSoup(str(main_div), 'html.parser')
    
    # 移除所有 script 标签及其内容
    for script in soup.find_all('script'):
        script.decompose()
    
    # 移除所有 style 标签及其内容
    for style in soup.find_all('style'):
        style.decompose()
    
    # 移除所有 svg 标签及其内容
    for svg in soup.find_all('svg'):
        svg.decompose()
    
    # img标签移除
    for img in soup.find_all('img'):
        img.decompose()
    
    # 移除所有 HTML 注释
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    # 移除内联样式
    for tag in soup.find_all(True):
        if isinstance(tag.attrs, dict) and 'style' in tag.attrs:
            tag.attrs.pop('style', None)
    
    # +++ 新增表格数据截取逻辑 +++
    for table in soup.find_all('table'):
        # 定位表格主体区域（通常包含在tbody中）
        tbody = table.find('tbody')
        if tbody:
            # 获取所有数据行（跳过表头）
            rows = tbody.find_all('tr')[2:]  # 保留前两行（索引0和1）
            for row in rows:
                row.decompose()

    # 优化后的空白处理（保留换行符）
    cleaned_html = soup.prettify()
    # 压缩连续空格为单个，保留换行符
    cleaned_html = ' '.join(cleaned_html.split()).replace('\n', '\n')
    # 处理标签间多余空格
    cleaned_html = cleaned_html.replace('> <', '><')
    
    return cleaned_html

if __name__ == "__main__":
    import os
    import sys
    
    def process_html_file(file_path):
        """处理指定HTML文件并保存清理结果"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaned = remove_unnecessary_content(content)
            
            # 保存清理后的文件
            new_path = os.path.splitext(file_path)[0] + "_cleaned.html"
            with open(new_path, 'w', encoding='utf-8') as f:
                # 确保写入的内容为字符串类型
                f.write(str(cleaned) if isinstance(cleaned, bytes) else cleaned)
            
            print(f"成功处理文件: {os.path.basename(file_path)}")
            print(f"清理后文件已保存至: {new_path}")
            print(f"原始大小: {len(content)} bytes → 清理后大小: {len(cleaned)} bytes")
            
        except Exception as e:
            print(f"处理文件时出错: {str(e)}")

    # 直接处理 sales_plan_body2.html（需要文件存在）
    if os.path.exists("sales_plan_body2.html"):
        process_html_file("sales_plan_body2.html")
    else:
        print("未找到 sales_plan_body2.html，请确保文件存在于当前目录")