# pages/base_page.py
import os
import logging
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # 导入Keys
import json

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_menu(self, menu_locator, submenu_locator=None, url_keyword=None):
        """
        通用菜单导航方法
        :param menu_locator: 主菜单定位元组
        :param submenu_locator: 子菜单定位元组（可选）
        :param url_keyword: URL中应包含的关键字（可选）
        """
        try:
            logging.info(f"点击主菜单: {menu_locator}")
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(menu_locator)
            ).click()
            if submenu_locator:
                logging.info(f"点击子菜单: {submenu_locator}")
                WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located(submenu_locator)
                ).click()
            if url_keyword:
                logging.info(f"等待URL包含: {url_keyword}")
                WebDriverWait(self.driver, 15).until(
                    EC.url_contains(url_keyword)
                )
        except Exception as e:
            logging.error(f"导航菜单异常: {str(e)}")
            raise

    def select_store_and_market(self):
        """选择店铺和市场"""
        from Base.base_element import BaseElement
        try:
            logging.info("点击店铺选择器")
            self.click_element(*BaseElement.STORE_LOCATOR)
            logging.info("点击市场选择器")
            self.click_element(*BaseElement.MARKET_LOCATOR)
        except Exception as e:
            logging.error(f"选择店铺或市场失败: {e}")
            raise

    def find_element(self, by, value, timeout=15):  # 延长超时时间并修改等待条件为可点击
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))  # 改为等待元素可点击
        )

    # def click_element(self, by, value, timeout=10):
    #     element = self.find_element(by, value, timeout)
    #     element.click()

    def click_element(self, by, value):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
        except Exception as e:
            #  fallback: 使用 JS 点击
            self.driver.execute_script("arguments[0].click();", element)
            print(f"通过 JS 点击元素：{value}，原异常：{e}")

    def send_keys(self, by, value, text, timeout=10):
        element = self.find_element(by, value, timeout)

        # # element.clear()
        # # 尝试使用JS清空，因为 standard clear() 可能无效
        # self.driver.execute_script("arguments[0].value = '';", element)

        # 尝试模拟键盘操作清空输入框
        element.send_keys(Keys.CONTROL + "a") # 全选
        element.send_keys(Keys.DELETE) # 删除
        element.send_keys(text)

    def wait_for_element_visibility(self, by, value, timeout=15):
        """等待元素可见"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def take_screenshot(self, filename_prefix):
        """截取当前页面截图并保存"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        screenshot_dir = os.path.join(os.path.dirname(__file__), '../screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f'{filename_prefix}_{timestamp}.png')
        try:
            self.driver.save_screenshot(screenshot_path)
            logging.info(f"截图已保存至：{screenshot_path}")
        except Exception as e:
            logging.error(f"截图失败: {str(e)}")

    def load_test_data(self, file_path, min_version='1.0'):
        """通用测试数据加载方法"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if not isinstance(data, list) or len(data) < 1:
                    raise ValueError("测试数据格式错误，应为非空数组")
                
                if 'data_version' not in data[0] or data[0]['data_version'] < min_version:
                    raise ValueError(f"数据版本过低，最低要求版本: {min_version}")
                
                return data[0]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.take_screenshot(f"load_data_error_{datetime.now().strftime('%Y%m%d%H%M%S')}")
            logging.error(f"加载测试数据失败: {str(e)}")
            raise

