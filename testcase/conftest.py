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


# 在已有 fixtures 后添加

@pytest.fixture(scope="session")
def module_urls(access_token):
    """获取各模块基础URL"""
    import requests
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 调用系统配置接口获取模块URL
    # 增加容错机制
    response = requests.get(
        "http://192.168.150.222:3066/erp/sys/permission/list",
        headers=headers,
        timeout=10  # 添加超时控制
    )
    response.raise_for_status()  # 自动抛出HTTP错误
    assert response.status_code == 200, "获取模块URL失败"
    
    return {
        "sales_plan": response.json()["salesPlanUrl"],
        "dashboard": response.json()["dashboardUrl"],
        "inventory": response.json()["inventoryUrl"]
    }
