# pages/sales_plan_page.py
from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 新增异常导入
import logging

class SalesPlanPage(BasePage):

    SALES_PLAN_URL = "/amzShipment/salesPlan"
    AMAZON_MENU = (By.XPATH, "//*[@id='app']/section/aside/div/ul/li[3]/div/span/span")
    SALES_PLAN_MENU = (By.CSS_SELECTOR, "#app > section > aside > div > ul > li.ant-menu-submenu.ant-menu-submenu-inline.ant-menu-submenu-open > ul > li:nth-child(2)") 
    ASIN_INPUT = (By.CSS_SELECTOR, "input[placeholder='请输入ASIN']")

    # 店铺市场:美时美刻/美国
    STORE_LOCATOR = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[3]")
    MARKET_LOCATOR = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[4]/div[1]/div[1]")

    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[title='搜索']")  # 搜索按钮
    SEARCH_RESULT = (By.CSS_SELECTOR, ".ant-table-row")  # 搜索结果表格
    ADD_SALES_PLAN_BUTTON = (By.XPATH, "//button[contains(text(),'添加销售计划')]")  # 添加按钮
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
        # 获取店铺、市场定位器
        # 直接使用硬编码定位器
        self.click_element(*self.STORE_LOCATOR)  # 选择店铺
        self.click_element(*self.MARKET_LOCATOR)  # 选择市场
        self.click_element(*self.SALES_PLAN_MENU)
        self.send_keys(*self.ASIN_INPUT, "B09G9DNNHV")  # 硬编码ASIN值
        # 点击搜索按钮
        self.click_element(*self.SEARCH_BUTTON)
        # 等待搜索结果
        self.wait_for_element_visibility(*self.SEARCH_RESULT)
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
    

