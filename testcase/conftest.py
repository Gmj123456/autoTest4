# testcase/conftest.py
import time
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, ERP_URL
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os

# 指定chromedriver.exe的路径，避免每次下载
# CHROME_DRIVER_PATH = r'../utils/chromedriver.exe'
# CHROME_DRIVER_PATH = r'D:\gmj\workSpaces\workSpaces_pycharm\autoTest1\utils\chromedriver.exe'
# 打印当前工作目录
print(f"当前工作目录: {os.getcwd()}")
# 获取当前脚本的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建 chromedriver 的相对路径
CHROME_DRIVER_PATH = os.path.join(script_dir, '..', 'utils', 'chromedriver.exe')
print(f"使用的 ChromeDriver 路径: {CHROME_DRIVER_PATH}")

@pytest.fixture(scope="function")
def driver():

    # 使用 Service 类指定 ChromeDriver 的位置
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()  # 设置全屏
    time.sleep(1)

    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.login(USERNAME, PASSWORD)

    # 定义登录成功后的 URL
    success_url = "http://192.168.150.222:3066/dashboard/analysis"

    try:
        # 等待页面 URL 变为登录成功后的 URL，最多等待 10 秒
        WebDriverWait(driver, 10).until(EC.url_to_be(success_url))
        print("登录成功")
        yield driver

    except TimeoutException:
        pytest.fail(f"登录失败，达到最大重试次数")

