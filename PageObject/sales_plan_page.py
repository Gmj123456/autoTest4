# pages/sales_plan_page.py
from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 新增异常导入
import logging
from datetime import datetime  # 新增datetime导入

class SalesPlanPage(BasePage):

    SALES_PLAN_URL = "/amzShipment/salesPlan"
    AMAZON_MENU = (By.XPATH, "//*[@id='app']/section/aside/div/ul/li[3]/div/span/span")
    SALES_PLAN_MENU = (By.CSS_SELECTOR, "#app > section > aside > div > ul > li.ant-menu-submenu.ant-menu-submenu-inline.ant-menu-submenu-open > ul > li:nth-child(2)") 
    ASIN_INPUT = (By.CSS_SELECTOR, "input[placeholder='请输入ASIN']")

    # 店铺市场:美时美刻/美国
    STORE_LOCATOR = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[3]")
    MARKET_LOCATOR = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[4]/div[1]/div[1]")

    SEARCH_BUTTON = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[2]/form/div/div[4]/span/button[1]")  # 搜索按钮（改为XPath定位，提高稳定性）
    SEARCH_RESULT = (By.XPATH, "//div[contains(@class,'ant-table-body')]//tr")  # 调整为更精确的表格行XPath定位
    # ADD_SALES_PLAN_BUTTON = (By.XPATH, "//button[contains(text(),'添加销售计划')]")  # 添加按钮
    ADD_SALES_PLAN_BUTTON = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[17]/div/a")  # 添加按钮
    # ADD_SALES_PLAN_BUTTON = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[17]/div/a")  # 添加按钮
    MONTH_SELECT = (By.CSS_SELECTOR, "input[placeholder='请选择月份']")  # 月份选择
    PLAN_QUANTITY_INPUT = (By.CSS_SELECTOR, "input[placeholder='请输入数量']")  # 数量输入
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'确认')]")  # 确认按钮
    

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
    


    def add_sales_plan(self, asin, months, quantities):
        """添加销售计划"""
        self.click_element(*self.STORE_LOCATOR)  # 选择店铺
        self.click_element(*self.MARKET_LOCATOR)  # 选择市场
        self.click_element(*self.SALES_PLAN_MENU)
        self.send_keys(*self.ASIN_INPUT, asin)  # 使用入参ASIN值
        # 点击搜索按钮
        self.click_element(*self.SEARCH_BUTTON)
        # 等待搜索结果（优化等待条件为元素存在并记录页面源码）
        try:
            self.wait_for_element_visibility(*self.SEARCH_RESULT, timeout=30)  # 原可见性等待
        except TimeoutException as e:
            self.take_screenshot(f"search_result_timeout_{datetime.now().strftime('%Y%m%d%H%M%S')}")  # 保存超时截图
            logging.error(f"搜索结果等待超时，当前页面源码：\n{self.driver.page_source[:2000]}")  # 记录前2000字符源码
            raise
        # 验证搜索结果数量（新增）
        search_results = self.driver.find_elements(*self.SEARCH_RESULT)
        assert len(search_results) > 0, "未找到搜索结果，请检查ASIN输入或搜索条件"
        # 点击添加销售计划按钮
        self.click_element(*self.ADD_SALES_PLAN_BUTTON)


        # 选择月份和数量（循环添加多个月份，从months数据中获取month和value）
        for month_data in months:
            self.click_element(*self.ADD_PLAN_BUTTON)
            self.send_keys(*self.MONTH_SELECT, month_data['month'])
            self.send_keys(*self.PLAN_QUANTITY_INPUT, month_data['value'])

        self.click_element(*self.CONFIRM_BUTTON)
    

