# autoTest1/element_location/save_html.py
from bs4 import BeautifulSoup

def save_body_content_to_file(driver, url, file='page_content.html'):
    """
    此函数用于从已登录的浏览器实例中获取指定 URL 的网页内容，
    提取 <body> 标签内容并保存到文件中。
    """
    try:
        driver.get(url)
        driver.implicitly_wait(10)  # 等待动态加载

        # 获取渲染后的内容
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        body = soup.find('body')

        if body:
            # 获取 <body> 内容并保存到文件
            with open(file, 'w', encoding='utf-8') as file:
                file.write(str(body))
            print(f"页面 <body> 内容已成功保存到 {file}")
        else:
            print("未找到 <body> 标签")

    except Exception as e:
        print(f"发生错误: {e}")