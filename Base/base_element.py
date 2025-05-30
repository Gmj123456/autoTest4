from selenium.webdriver.common.by import By

import json
import os
from selenium.webdriver.common.by import By

class BaseElement:
    """
    动态读取店铺和市场
    """
    # 动态读取store名称
    @staticmethod
    def get_store_name():
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'TestCase', 'TestData', 'sales_plan_month.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[0]['store'] if data and 'store' in data[0] else ''
    # 动态读取marketplace名称
    @staticmethod
    def get_marketplace():
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'TestCase', 'TestData', 'sales_plan_month.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[0]['marketplace'] if data and 'marketplace' in data[0] else ''
    # 动态读取店铺和市场
    STORE_LOCATOR = (By.XPATH, f"//div[@role='tab' and contains(@class, 'ant-tabs-tab') and text()='{get_store_name()}']")
    MARKET_LOCATOR = (By.XPATH, f"//div[contains(@class, 'country-item') and contains(text(), '{get_marketplace()}')]")


    """
    通用组件的定位方式
    """
    ASIN_INPUT = (By.CSS_SELECTOR, "input[placeholder='请输入ASIN']")  # ASIN输入框
    SEARCH_BUTTON = (By.XPATH, "//button[contains(@class, 'ant-btn-primary') and span[text()='查询']]")  # 搜索按钮
    MESSAGE = (By.CSS_SELECTOR,"body > div.ant-message > span > div > div > div > span")#消息提示