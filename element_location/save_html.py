# autoTest1/element_location/save_html.py
from bs4 import BeautifulSoup

def save_body_content_to_file(driver, url, file_path='page_content.html'):
    """
    此函数用于从已登录的浏览器实例中获取指定 URL 的网页内容，
    提取 <body> 标签内容并保存到文件中。

    :param driver: 已登录的浏览器驱动实例
    :param url: 要访问的网页的 URL。
    :param file_path: 保存 <body> 内容的文件路径，默认为 'page_content.html'。
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
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(body))
            print(f"页面 <body> 内容已成功保存到 {file_path}")
        else:
            print("未找到 <body> 标签")

    except Exception as e:
        print(f"发生错误: {e}")


def batch_save_pages(driver, url_list, output_dir="html_output"):
    """
    批量保存多个页面的<body>内容
    
    :param driver: 已登录的浏览器驱动实例
    :param url_list: 要保存的URL列表
    :param output_dir: 输出目录路径（默认：html_output）
    """
    from pathlib import Path
    from urllib.parse import urlparse
    import re
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for url in url_list:
        try:
            # 生成安全文件名（修复缺失的变量）
            parsed_url = urlparse(url)
            path = parsed_url.path or "/index"  # 处理空路径
            file_name = re.sub(r'[^a-zA-Z0-9]', '_', path).strip('_') + '.html'
            
            # 处理多下划线问题
            file_name = re.sub(r'_+', '_', file_name)
            file_path = str(Path(output_dir) / file_name)
            
            # 调用现有函数
            save_body_content_to_file(driver, url, file_path)
            print(f"成功保存: {url} -> {file_path}")
            
        except Exception as e:
            print(f"处理 {url} 失败: {str(e)}")

# # 修改测试用例部分
# if __name__ == "__main__":
#     from pages.login_page import LoginPage
#     from selenium import webdriver
    
#     # 初始化浏览器驱动并登录
#     driver = webdriver.Chrome()
#     login_page = LoginPage(driver)
    
#     try:
#         # 执行登录（需要替换实际账号密码）
#         if login_page.login("guomj", "123456"):
#             # 示例URL列表（使用相对路径）
#             test_urls = [
#                 "/amzShipment/salesPlan",
#                 "/amzShipment/inventory"
#             ]
            
#             # 拼接完整URL（根据实际环境配置）
#             base_url = "http://192.168.150.222:3066"
#             full_urls = [base_url + path for path in test_urls]
            
#             # 调用批量保存函数
#             batch_save_pages(driver, full_urls)
            
#     finally:
#         driver.quit()