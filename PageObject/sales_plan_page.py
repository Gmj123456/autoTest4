# pages/sales_plan_page.py
from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 新增异常导入
import logging
from datetime import datetime  # 新增datetime导入
import time

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
    # ADD_SALES_PLAN_BUTTON = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[17]/div/a")  # 添加按钮
    ADD_SALES_PLAN_BUTTON = (By.XPATH, "/html/body/div[1]/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[17]/div/a")  # 添加按钮
    # ADD_SALES_PLAN_BUTTON = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[17]/div/a")  # 添加按钮
    # MONTH_SELECT = (By.CSS_SELECTOR, "input[placeholder='请选择月份']")  # 月份选择
    # MONTH_SELECT = (By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div[2]/div/div/form/div/div[2]/div/div[2]/div/span/span/div/input")  # 月份选择
    MONTH_SELECT = (By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div[2]/div/div/form/div/div[2]/div/div[2]/div/span/span/div/input")  # 月份选择
    # PLAN_QUANTITY_INPUT = (By.CSS_SELECTOR, "input[placeholder='请输入数量']")  # 数量输入
    PLAN_QUANTITY_INPUT = (By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div[2]/div/div/form/div/div[5]/div/div/div[2]/div[1]/div[2]/table/tbody/tr/td[4]/div/div/div[2]/input")  # 数量输入
    SAVE_AND_CONTINUE_BUTTON = (By.XPATH,"/html/body/div[7]/div/div[2]/div/div[2]/div[3]/button[2]")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'确认')]")  # 确认按钮
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'ant-message-success')]/span[contains(text(),'操作成功')]")  # 成功提示


    XIANGGUI = (By.XPATH,"//*[@id='app']/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[8]/div/div/a/span")

    def is_success_message_displayed(self):
        """验证成功提示是否显示"""
        try:
            return self.wait_for_element_visibility(*self.SUCCESS_MESSAGE).is_displayed()
        except TimeoutException:
            return False

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
    


    def add_sales_plan(self, asin, months, value):
        """添加销售计划"""
        self.click_element(*self.STORE_LOCATOR)  # 选择店铺
        self.click_element(*self.MARKET_LOCATOR)  # 选择市场
        self.click_element(*self.SALES_PLAN_MENU)
        self.send_keys(*self.ASIN_INPUT, asin)  # 使用入参ASIN值
        # 点击搜索按钮
        self.click_element(*self.SEARCH_BUTTON)

        # 点击添加销售计划按钮
        self.click_element(*self.ADD_SALES_PLAN_BUTTON)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.MONTH_SELECT)
        )


        # 选择月份和数量（循环添加多个月份，从months数据中获取month和value）
        for i, month_data in enumerate(months):
            # self.click_element(*self.ADD_PLAN_BUTTON)
            self.send_keys(*self.MONTH_SELECT, month_data['month'])
            # 直接从月份字典获取value值
            for month_data in months:
                self.send_keys(*self.PLAN_QUANTITY_INPUT, str(month_data['value']))
            self.click_element(*self.SAVE_AND_CONTINUE_BUTTON)

        self.click_element(*self.CONFIRM_BUTTON)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
    

