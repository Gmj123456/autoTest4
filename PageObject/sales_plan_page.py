# pages/sales_plan_page.py
from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 新增异常导入
import logging
from Base.config import ASIN

class SalesPlanPage(BasePage):
    SALES_PLAN_URL = "/amzShipment/salesPlan"
    # AMAZON = (By.CSS_SELECTOR, "li[title='Amazon']")  # 更稳定的CSS选择器
    # SALES_PLAN_MENU = (By.XPATH, "//span[contains(text(),'销售计划')]")  # 使用文本包含匹配
    AMAZON_MENU = (By.XPATH, "//*[@id='app']/section/aside/div/ul/li[3]/div/span/span")
    SALES_PLAN_MENU = (By.CSS_SELECTOR, "#app > section > aside > div > ul > li.ant-menu-submenu.ant-menu-submenu-inline.ant-menu-submenu-open > ul > li:nth-child(2)") 
    ASIN_INPUT = (By.CSS_SELECTOR, "input[placeholder='请输入ASIN']")
    

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

    def add_sales_plan(self, asin, months, quantities):
        """添加销售计划"""
        # 获取店铺、市场定位器
        store_locator = self.get_locator_by_text('path/to/sales_plan_stroe_location.json', '美时美刻')
        market_locator = self.get_locator_by_text('path/to/sales_plan_stroe_location.json', '美国')
        if store_locator and market_locator:
            self.click_element(*store_locator)  # 选择店铺
            self.click_element(*market_locator)  # 选择市场
        else:
            logging.error("无法找到店铺或市场的定位器")
            raise ValueError("无法找到店铺或市场的定位器")

        self.click_element(*self.SALES_PLAN_MENU)
        # 之前已经获取了 store_locator，这里直接使用之前获取的变量
        if store_locator:
            self.click_element(*store_locator)  # 选择店铺
        self.click_element(*market_locator)  # 选择市场
        self.send_keys(*self.ASIN_INPUT, ASIN)  # 输入ASIN
        # 点击搜索按钮
        self.click_element(*self.SEARCH_BUTTON)
        # 等待搜索结果
        self.wait_for_element_visibility(*self.SEARCH_RESULT   )
        # 点击添加销售计划按钮
        self.click_element(*self.ADD_SALES_PLAN_BUTTON)
        # 等待销售计划页面加载完成
        self.wait_for_element_visibility(*self.ADD_PLAN_BUTTON)

        # 选择月份和数量（循环添加多个月份，具体月份和SKU、数量从testdata文件夹下的sales_plan_month.json中获取）
        for month, quantity in zip(months, quantities):
            self.click_element(*self.ADD_PLAN_BUTTON)
            self.send_keys(*self.MONTH_SELECT, month)
            self.send_keys(*self.PLAN_QUANTITY_INPUT, quantity)

        self.click_element(*self.CONFIRM_BUTTON)
    

