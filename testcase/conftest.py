import time
import pytest
import logging
from selenium import webdriver
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD
from selenium.webdriver.chrome.service import Service
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前脚本的绝对路径
script_dir = Path(__file__).resolve().parent
# 构建 chromedriver 的相对路径
CHROME_DRIVER_PATH = script_dir.parent / 'utils' / 'chromedriver.exe'
logging.info(f"使用的 ChromeDriver 路径: {CHROME_DRIVER_PATH}")


@pytest.fixture(scope="function")
def driver():
    # 使用 Service 类指定 ChromeDriver 的位置
    service = Service(str(CHROME_DRIVER_PATH))
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()  # 设置全屏
    time.sleep(1)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    result = login_page.login(USERNAME, PASSWORD)

    if result:
        logging.info("登录成功")
        yield driver
    else:
        pytest.fail("登录失败")
