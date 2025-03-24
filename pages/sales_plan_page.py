# pages/sales_plan_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 新增异常导入
import logging

class SalesPlanPage(BasePage):
    # AMAZON = (By.CSS_SELECTOR, "li[title='Amazon']")  # 更稳定的CSS选择器
    # SALES_PLAN_MENU = (By.XPATH, "//span[contains(text(),'销售计划')]")  # 使用文本包含匹配
    AMAZON_MENU = (By.XPATH, "//*[@id='app']/section/aside/div/ul/li[3]/div/span/span")
    SALES_PLAN_MENU = (By.CSS_SELECTOR, "#app > section > aside > div > ul > li.ant-menu-submenu.ant-menu-submenu-inline.ant-menu-submenu-open > ul > li:nth-child(2)") 

    SALES_PLAN_URL = "/amzShipment/salesPlan"

    def navigate_to_sales_plan(self):
        """导航到销售计划页面（添加显式等待和重试机制）"""
        try:
            # 确保元素可交互
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.AMAZON_MENU)
            ).click()
            
            # 等待菜单项可见
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.SALES_PLAN_MENU)
            ).click()
            
            # 等待URL包含目标路径
            WebDriverWait(self.driver, 15).until(
                EC.url_contains(self.SALES_PLAN_URL)
            )
            
        except TimeoutException as e:
            logging.error(f"导航到销售计划页面超时: {str(e)}")
            raise
        except NoSuchElementException as e:
            logging.error(f"元素定位失败: {str(e)}")
            raise
    
    def get_current_url(self):
        """获取当前页面URL"""
        return self.driver.current_url


    
    def add_single_plan(self, month: str, quantity: str):
        """添加单个销售计划"""
        self.click_element(*self.ADD_PLAN_BUTTON)
        
        # 带参数的定位器使用
        month_locator = (self.MONTH_LINK[0], self.MONTH_LINK[1].format(month))
        self.click_element(*month_locator)
        
        self.send_keys(*self.PLAN_QUANTITY_INPUT, quantity)
        self.click_element(*self.CONFIRM_BUTTON)

    def __init__(self, driver):
        super().__init__(driver)

    def add_sales_plan(self, asin, months, quantities):
        self.click_element(*self.SALES_PLAN_MENU)
        self.click_element(*self.STORE_SELECT)  # 选择店铺
        self.click_element(*self.MARKET_SELECT)  # 选择市场
        self.send_keys(*self.ASIN_INPUT, asin)
        self.click_element(*self.SEARCH_BUTTON)

        for month, quantity in zip(months, quantities):
            self.click_element(*self.ADD_PLAN_BUTTON)
            self.send_keys(*self.MONTH_SELECT, month)
            self.send_keys(*self.PLAN_QUANTITY_INPUT, quantity)

        self.click_element(*self.CONFIRM_BUTTON)
    

