import pytest
import requests
import logging
from Base.utils.logger import setup_logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PageObject.login_page import LoginPage
from Base.config import USERNAME, PASSWORD
import datetime

# 调用统一的日志配置
logger = setup_logging()

from Base.config import CHROME_DRIVER_PATH
# 记录使用的 ChromeDriver 路径
logging.info(f"使用的 ChromeDriver 路径: {CHROME_DRIVER_PATH}")
"""
此 fixture 用于创建一个 Chrome 浏览器实例，使用测试账号登录，并返回登录后的驱动实例。
每个测试函数执行前都会重新创建浏览器实例并登录。
"""
@pytest.fixture(scope="function")
def logged_in():
    # 创建 Chrome 浏览器服务实例
    service = Service(str(CHROME_DRIVER_PATH))
    # 创建 Chrome 浏览器驱动实例
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    # 创建登录页面实例
    login_page = LoginPage(driver)
    # 使用测试账号进行登录
    result = login_page.login(USERNAME, PASSWORD)
    # 检查登录是否成功，若失败则终止测试
    if not result:
        pytest.fail("登录失败")
        
    yield driver



    # 关闭浏览器
    logging.info("关闭浏览器")
    driver.quit()

import json
from pathlib import Path

@pytest.fixture(scope="function")
def menu_urls():
    # 从TestData/menu.json读取菜单URL数据
    test_data_path = Path(__file__).parent / "TestData" / "menu.json"
    with open(test_data_path, "r", encoding="utf-8") as f:
        menu_data = json.load(f)
    return menu_data

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """记录测试用例开始时间"""
    start_time = datetime.datetime.now()
    logger.info(f"Test case {item.name} started at {start_time}")
    outcome = yield

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """记录测试用例结束时间"""
    outcome = yield
    end_time = datetime.datetime.now()
    logger.info(f"Test case {item.name} ended at {end_time}")