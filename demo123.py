import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By


url = "http://192.168.150.222:3066/"  # 替换为实际页面URL

CHROME_DRIVER_PATH = r'D:\gmj\workSpaces\workSpaces_pycharm\autoTest1\utils\chromedriver.exe'

# 使用 Service 类指定 ChromeDriver 的位置
service = Service(str(CHROME_DRIVER_PATH))
driver = webdriver.Chrome(service=service)


driver.get(url)
driver.maximize_window()  # 设置全屏
time.sleep(2)

driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[1]/div/div/span/input").send_keys("guomj")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[2]/div/div/span/input").send_keys("qwe123")



time.sleep(10)


try:
    # 获取localStorage中的所有数据
    localStorage = driver.execute_script('return window.localStorage;')

    # 尝试从 localStorage 中获取 pro__Access-Token 的值
    access_token_str = localStorage.get('pro__Access-Token')
    if access_token_str:
        try:
            # 将获取到的字符串解析为 Python 字典
            access_token_dict = json.loads(access_token_str)
            # 从字典中提取 "value" 键对应的值
            value = access_token_dict.get("value")
            if value:
                print(f"Token的值为: {value}")
            else:
                print("pro__Access-Token 中不存在 value 字段")
        except json.JSONDecodeError:
            print("无法将 pro__Access-Token 的值解析为 JSON 格式")
    else:
        # 如果未找到 pro__Access-Token，打印提示信息
        print("未找到 pro__Access-Token")


except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # 关闭浏览器
    driver.quit()