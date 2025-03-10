# testcase/conftest.py
import time
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, ERP_URL
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    # 定义登录成功后的 URL
    success_url = "http://192.168.150.222:3066/dashboard/analysis"

    try:
        # 等待页面 URL 变为登录成功后的 URL，最多等待 10 秒
        WebDriverWait(driver, 10).until(EC.url_to_be(success_url))
        print("登录成功")
    except TimeoutException:
        pytest.fail(f"登录失败，当前页面 URL 为: {driver.current_url}")

    yield driver