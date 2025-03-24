import pytest
from pages.sales_plan_page import SalesPlanPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import ERP_URL
from selenium.webdriver.common.action_chains import ActionChains
import logging
from selenium.common.exceptions import TimeoutException  # 新增导入
import pdb
import time

class TestSalesPlan:
    def test_sales_plan1(self, logged_in):
        """验证销售计划菜单跳转功能"""
        AMAZON_MENU = (By.XPATH, "//*[@id='app']/section/aside/div/ul/li[3]/div/span/span")
        SALES_PLAN = (By.CSS_SELECTOR, "#app > section > aside > div > ul > li.ant-menu-submenu.ant-menu-submenu-inline.ant-menu-submenu-open > ul > li:nth-child(2)") 


        try:
           
            amazon_element = WebDriverWait(logged_in, 15).until(
                EC.element_to_be_clickable(AMAZON_MENU)
            )
            amazon_element.click() 
            logging.info("已点击Amazon菜单")
            # 点击销售计划子菜单
            WebDriverWait(logged_in, 10).until(
                EC.element_to_be_clickable(SALES_PLAN)
            ).click()
            logging.info("已点击销售计划子菜单")
            # 验证URL包含目标路径
            WebDriverWait(logged_in, 15).until(
                EC.url_contains("/amzShipment/salesPlan")
            )
            

            time.sleep(20)


        except TimeoutException as e:
            logging.error(f"操作超时，当前页面源码：\n{logged_in.page_source[:2000]}")
            pytest.fail(f"测试失败：{str(e)}")
