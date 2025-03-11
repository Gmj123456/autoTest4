import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import logging
import time


# 目标URL
url = "http://192.168.150.222:3066/"  # 替换为实际页面URL

CHROME_DRIVER_PATH = r'D:\gmj\workSpaces\workSpaces_pycharm\autoTest1\utils\chromedriver.exe'

# 使用 Service 类指定 ChromeDriver 的位置
service = Service(str(CHROME_DRIVER_PATH))
driver = webdriver.Chrome(service=service)
driver.maximize_window()  # 设置全屏

driver.get(url)

time.sleep(10)

# 展开所有折叠项
expand_buttons = driver.find_elements(By.CLASS_NAME, 'ant-table-row-expand-icon')
for button in expand_buttons:
    button.click()

# 获取展开后的HTML
expanded_html = driver.page_source
driver.quit()

# 解析HTML
soup = BeautifulSoup(expanded_html, 'html.parser')
menu_structure = {}
current_parent = None

for tr in soup.find_all('tr'):
    # 确定菜单层级
    indent_span = tr.find('span', class_='ant-table-row-indent')
    level = -1
    if indent_span:
        padding = indent_span.get('style', '')
        if 'padding-left: 0px;' in padding:
            level = 0
        elif 'padding-left: 20px;' in padding:
            level = 1

    # 提取菜单名称和路径
    tds = tr.find_all('td')
    if len(tds) < 6:
        continue
    name = tds[1].get_text(strip=True)
    path = tds[5].get_text(strip=True)

    # 构建菜单结构
    if level == 0:
        menu_structure[name] = {'path': path, 'children': []}
        current_parent = name
    elif level == 1 and current_parent:
        menu_structure[current_parent]['children'].append({'name': name, 'path': path})

# 将菜单结构转换为 JSON 格式
menu_json = json.dumps(menu_structure, ensure_ascii=False, indent=2)
print(menu_json)
