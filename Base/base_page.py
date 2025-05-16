# pages/base_page.py
import os
import logging
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value, timeout=15):  # 延长超时时间并修改等待条件为可点击
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))  # 改为等待元素可点击
        )

    def click_element(self, by, value, timeout=10):
        element = self.find_element(by, value, timeout)
        element.click()

    def send_keys(self, by, value, text, timeout=10):
        element = self.find_element(by, value, timeout)
        element.clear()
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
