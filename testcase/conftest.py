# testcase/conftest.py
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, ERP_URL

# 指定 chromedriver.exe 的路径
CHROME_DRIVER_PATH = "./utils/chromedriver.exe"

@pytest.fixture(scope="function")
def driver():
    # 使用 Service 类指定 chromedriver.exe 的位置
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
    yield driver