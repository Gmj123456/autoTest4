# testcase/conftest.py
import time

import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, ERP_URL
# import sys
# import os
#
# # # 将项目根目录添加到 Python 搜索路径
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# # print("sys.path:", sys.path)  # 新增打印
#
# # 替换为你的实际项目路径
# sys.path.append(r"D:\gmj\workSpaces\workSpaces_pycharm\autoTest")

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()  # 设置全屏
    time.sleep(1)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.login(USERNAME, PASSWORD)
    yield driver