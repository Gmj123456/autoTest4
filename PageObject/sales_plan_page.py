# pages/sales_plan_page.py
from Base.base_page import BasePage
from Base.base_element import BaseElement
from TestCase.element_locator.sales_plan_elements import SalesPlanElements
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from datetime import datetime
import time
import os

class SalesPlanPage(BasePage):

    def navigate_to_sales_plan(self):
        """导航到销售计划页面（兼容旧用例）"""
        self.navigate_to_menu(
            SalesPlanElements.MENU_AMAZON,
            SalesPlanElements.SALES_PLAN_MENU,
            SalesPlanElements.SALES_PLAN_URL
        )

    def add_sales_plan(self, asin):
        """添加销售计划"""
        try:
            self.select_store_and_market()
            logging.info("点击销售计划菜单")
            self.click_element(*SalesPlanElements.SALES_PLAN_MENU)

            logging.info(f"输入ASIN: {asin}")
            self.send_keys(*BaseElement.ASIN_INPUT, asin)  # 使用入参ASIN值
            logging.info("点击搜索按钮")
            self.click_element(*BaseElement.SEARCH_BUTTON)# 点击搜索按钮
            logging.info("点击创建需求按钮")
            self.click_element(*SalesPlanElements.ADD_SALES_PLAN_BUTTON)# 点击创建需求按钮
            # 等待月份选择框出现
            logging.info("等待月份选择框出现")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(SalesPlanElements.MONTH_SELECT)
            )
            logging.info("点击月份选择框")
            self.click_element(*SalesPlanElements.MONTH_SELECT)   # 点击月份选择框
            # 等待弹窗月份选项出现
            logging.info("等待弹窗月份选项出现")
            WebDriverWait(self.driver, 10).until(
                # EC.element_to_be_clickable(SalesPlanElements.SELECT_MONTH_5)
                EC.element_to_be_clickable(SalesPlanElements.get_month_option("五月"))
            )
            logging.info("点击五月选项")
            self.click_element(*SalesPlanElements.SELECT_MONTH_5)
            self.click_element(*SalesPlanElements.get_month_option("五月")) 

            logging.info("输入计划数量1000")
            self.send_keys(*SalesPlanElements.PLAN_QUANTITY_INPUT, 1000)
            logging.info("点击保存并继续按钮")
            self.click_element(*SalesPlanElements.SAVE_AND_CONTINUE_BUTTON)

            try:
                logging.info("等待提示消息出现")
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(BaseElement.MESSAGE))
                success_message = self.find_element(*BaseElement.MESSAGE).text
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
                logging.info("等待月份选择框出现")
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(SalesPlanElements.MONTH_SELECT)
                )
                logging.info("点击月份选择框")
                self.click_element(*SalesPlanElements.MONTH_SELECT)
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(month_locator)
                )
                # 月份选择逻辑
                month_locator = self.get_month_locator(month)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(month_locator))
                self.click_element(*month_locator)
                
                # 修正OCR处理逻辑
                self.recognize_captcha()
                self.click_element(*month_locator)
                self.send_keys(*SalesPlanElements.PLAN_QUANTITY_INPUT, case["input"])
                self.click_element(*SalesPlanElements.SAVE_AND_CONTINUE_BUTTON)
                try:
                    message_element = BaseElement.MESSAGE  # 统一使用MESSAGE元素定位器
                    
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(message_element))
                    message_text = self.find_element(*message_element).text
                    logging.info(f"获取提示信息: {message_text}")
                    
                    assertion_status = "fail"
                    if case['expected']['success']:
                        if "添加成功" in message_text:
                            assertion_status = "pass"
                    else:
                        if "请添加sku计划数量" in message_text:
                            assertion_status = "pass"
                            
                    results.append({"input": case["input"], "expected": case["expected"], "actual": message_text, "result": assertion_status})
                except Exception as e:
                    logging.error(f"获取或断言提示信息失败: {str(e)}")
                    results.append({"input": case["input"], "expected": case["expected"], "actual": str(e), "result": "fail"})
            except Exception as e:
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                screenshot_dir = './screenshots'
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f'add_sales_plan_error_{timestamp}.png')
                self.driver.save_screenshot(screenshot_path)
                logging.error(f"添加销售计划异常，已截图: {screenshot_path}, 错误信息: {str(e)}")
                results.append({"input": case["input"], "expected": case["expected"], "actual": str(e), "result": "fail"})
            time.sleep(2)  # 每轮执行后等待2秒
        return results

    
    # 对照商品

    # 对照耗材

    # 修改箱规

    # 删除销售计划

    # 编辑销售计划

    def add_sales_plan_for_months(self, months_data):
        """连续添加多个月份的销售计划"""
        all_results = []
        for month_data in months_data:
            month_name = month_data['month']
            quantity_cases = month_data['quantity_cases']
            logging.info(f"开始添加 {month_name} 的销售计划")
            month_locator = SalesPlanElements.get_month_option(month_name)
            results = self.add_sales_plan_with_quantity_cases(month_locator, quantity_cases)
            for r in results:
                r['month'] = month_name  # 添加月份信息到结果中
            all_results.extend(results)
            logging.info(f"完成添加 {month_name} 的销售计划")
        return all_results



