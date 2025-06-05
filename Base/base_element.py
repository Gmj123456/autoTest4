from selenium.webdriver.common.by import By

import json
import os
from selenium.webdriver.common.by import By

class BaseElement:


    MENU_AMAZON = (By.XPATH, "//*[@role='menu']//span[text()='Amazon发货']") # Amazon发货菜单



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
    MONTH_SELECT = (By.XPATH, "//div[@class='ant-modal-content']//input[@placeholder='请选择月份']")  # 月份选择框
    SKU_INPUT = (By.CSS_SELECTOR, "input[placeholder='请输入SKU名称']")  # SKU名称输入框
    SELECT_FACTORY = (By.XPATH, "//div[contains(@class, 'ant-select') and .//div[text()='请选择生产工厂']]")  # 生产工厂选择框
    SEARCH_BUTTON = (By.XPATH, "//button[contains(@class, 'ant-btn-primary') and span[text()='查询']]")  # 查询按钮
    MESSAGE = (By.CSS_SELECTOR,"body > div.ant-message > span > div > div > div > span")  # 消息提示
