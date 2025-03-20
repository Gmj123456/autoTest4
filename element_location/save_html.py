from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def save_body_content_to_file(url, file_path='page_content.html'):
    """
    此函数用于从指定的 URL 获取网页内容，提取 <body> 标签内容并保存到文件中。

    :param url: 要访问的网页的 URL。
    :param file_path: 保存 <body> 内容的文件路径，默认为 'page_content.html'。
    """
    options = Options()
    options.add_argument("--headless")  # 无头模式
    driver = webdriver.Chrome(options=options)

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

    finally:
        driver.quit()

# # 调用示例
# if __name__ == "__main__":
#     target_url = "http://124.222.178.125:3006/"
#     save_body_content_to_file(target_url)