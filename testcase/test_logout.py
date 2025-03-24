import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from config.config import LOGIN_SUCCESS_URL

class TestLogout():
    def test_logout(self, logged_in):
        driver = logged_in
        login_page = LoginPage(driver)
        
        # 执行退出操作
        assert login_page.logout() is True
        
        # 验证退出后状态
        try:
            # 等待URL跳转并验证登录页面元素
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(login_page.USERNAME_INPUT)
            )
            assert "login" in driver.current_url.lower()
            
            # 验证localStorage中的token是否失效
            token = driver.execute_script('return window.localStorage.getItem("pro__Access-Token");')
            assert token is None
            
        except Exception as e:
            pytest.fail(f"退出登录验证失败: {str(e)}")