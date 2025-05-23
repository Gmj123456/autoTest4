# pages/sales_plan_page.py
from Base.base_page import BasePage
from Base.base_element import BaseElement
from TestCase.element_locator.sales_plan_elements import SalesPlanElements
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 新增异常导入
import logging
from datetime import datetime  # 新增datetime导入
import time
import os

class SalesPlanPage(BasePage):

    def navigate_to_sales_plan(self):
        """导航到销售计划页面（添加显式等待和重试机制）"""
        try:
            # 确保元素可交互
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(SalesPlanElements.MENU_AMAZON)
            ).click()
            
            # 等待菜单项可见
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(SalesPlanElements.SALES_PLAN_MENU)
            ).click()
            
            # 等待URL包含目标路径
            WebDriverWait(self.driver, 15).until(
                EC.url_contains(SalesPlanElements.SALES_PLAN_URL)
            )
            
        except TimeoutException as e:
            logging.error(f"导航到销售计划页面超时: {str(e)}")
            raise
        except NoSuchElementException as e:
            logging.error(f"元素定位失败: {str(e)}")
            raise
    


    # def add_sales_plan(self, asin, months, value):
    def add_sales_plan(self, asin):
        """添加销售计划"""
        try:
            self.click_element(*BaseElement.STORE_LOCATOR)  # 选择店铺
            self.click_element(*BaseElement.MARKET_LOCATOR)  # 选择市场
            self.click_element(*SalesPlanElements.SALES_PLAN_MENU)
            self.send_keys(*BaseElement.ASIN_INPUT, asin)  # 使用入参ASIN值
            self.click_element(*BaseElement.SEARCH_BUTTON)# 点击搜索按钮
            self.click_element(*SalesPlanElements.ADD_SALES_PLAN_BUTTON)# 点击创建需求按钮
            # 等待月份选择框出现
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(SalesPlanElements.MONTH_SELECT)
            )
            self.click_element(*SalesPlanElements.MONTH_SELECT)   # 点击月份选择框
            # 等待弹窗月份选项出现
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(SalesPlanElements.SELECT_MONTH_5)
            )
            self.click_element(*SalesPlanElements.SELECT_MONTH_5) 


            self.send_keys(*SalesPlanElements.PLAN_QUANTITY_INPUT, 1000)
            self.click_element(*SalesPlanElements.SAVE_AND_CONTINUE_BUTTON)

            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(BaseElement.SUCCESS_MESSAGE))
                success_message = self.find_element(*BaseElement.SUCCESS_MESSAGE).text
                logging.info(f"保存成功提示: {success_message}")
                return success_message
            except Exception as e:
                logging.error(f"获取成功提示信息失败: {str(e)}")
                return ""
                
            # self.click_element(*SalesPlanElements.CONFIRM_BUTTON)
            # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(SalesPlanElements.SUCCESS_MESSAGE))
        except Exception as e:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            screenshot_dir = './screenshots'
            
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f'add_sales_plan_error_{timestamp}.png')
            self.driver.save_screenshot(screenshot_path)
            logging.error(f"添加销售计划异常，已截图: {screenshot_path}, 错误信息: {str(e)}")
            raise

    
    

    def add_sales_plan_with_quantity_cases(self, month_locator, quantity_cases):
        """
        month_locator: 月份选择器元组（如SalesPlanElements.get_month_option("五月")）
        quantity_cases: [{"input":..., "expected":...}, ...]
        """
        results = []
        for case in quantity_cases:
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(SalesPlanElements.MONTH_SELECT)
                )
                self.click_element(*SalesPlanElements.MONTH_SELECT)
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(month_locator)
                )
                self.click_element(*month_locator)
                self.send_keys(*SalesPlanElements.PLAN_QUANTITY_INPUT, case["input"])
                self.click_element(*SalesPlanElements.SAVE_AND_CONTINUE_BUTTON)
                try:
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(BaseElement.SUCCESS_MESSAGE))
                    success_message = self.find_element(*BaseElement.SUCCESS_MESSAGE).text
                    logging.info(f"保存成功提示: {success_message}")
                    results.append({"input": case["input"], "expected": case["expected"], "actual": success_message, "result": "pass"})
                except Exception as e:
                    logging.error(f"获取成功提示信息失败: {str(e)}")
                    results.append({"input": case["input"], "expected": case["expected"], "actual": str(e), "result": "fail"})
            except Exception as e:
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                screenshot_dir = './screenshots'
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f'add_sales_plan_error_{timestamp}.png')
                self.driver.save_screenshot(screenshot_path)
                logging.error(f"添加销售计划异常，已截图: {screenshot_path}, 错误信息: {str(e)}")
                results.append({"input": case["input"], "expected": case["expected"], "actual": str(e), "result": "fail"})
        return results

    
    

