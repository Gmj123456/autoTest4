import pytest
from selenium.webdriver import Chrome
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage  # 新增导入
from config.config import USERNAME, PASSWORD  # 新增导入

@pytest.fixture(scope="module")
def browser():
    # 构建chromedriver绝对路径
    # 删除本地路径构建
    # project_root = Path(__file__).parent.parent
    # driver_path = project_root / 'utils' / 'chromedriver.exe'
    
    # 改为从config导入
    from config.config import CHROME_DRIVER_PATH
    driver_path = CHROME_DRIVER_PATH
    
    # 初始化浏览器实例
    service = Service(str(driver_path))
    driver = Chrome(service=service)
    # 增加窗口最大化操作
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_get_access_token_with_real_login(browser):
    login_page = LoginPage(browser)  # 新增实例化
    
    browser.save_screenshot("debug_login.png")
    if login_page.login(USERNAME, PASSWORD):
        browser.save_screenshot("debug_loggedin.png")
        # 获取并验证token
        token = login_page.get_access_token()
        assert token is not None, "应该能获取到有效token"
        assert len(token) > 30, "token长度应该大于30个字符"
        
        # 验证token有效性（示例）
        assert token.startswith("eyJ"), "token应该符合JWT格式"
    else:
        pytest.fail("登录失败导致无法获取token")

def test_get_access_token_without_login(browser):
    """测试未登录状态的token获取"""
    from pages.login_page import LoginPage
    
    login_page = LoginPage(browser)
    browser.delete_all_cookies()
    browser.get("about:blank")  # 清空上下文
    
    token = login_page.get_access_token()
    assert token is None, "未登录时应返回None"