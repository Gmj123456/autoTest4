# autoTest1/TestCase/test_sales_plan.py
import pytest
import logging
import time

from selenium.webdriver.common.by import By

from Base.base_page import BasePage
from Base.config import ERP_URL
from Base.base_element import BaseElement
from PageObject.sales_plan_page import SalesPlanPage
import logging
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestCase.conftest import logged_in
import json
from TestCase.elements_locator import elements_salesPlan
from TestCase.elements_locator.elements_salesPlan import SalesPlanElements


class TestSalesPlan:
    def test_menu_navigation(self, logged_in, menu_urls):
        """验证销售计划菜单跳转"""
        # 添加会话状态检查
        try:
            # 添加基础健康检查
            logged_in.execute_script("return document.readyState;")
        except Exception as e:
            pytest.fail(f"浏览器会话已丢失: {str(e)}")

        # 增加显式等待确保页面稳定
        WebDriverWait(logged_in, 10).until(
            lambda d: d.execute_script("return document.readyState === 'complete'")
        )
        
        assert menu_urls is not None, "菜单URL数据未正确加载"
        assert "销售计划" in menu_urls, "菜单数据中缺少销售计划项"

        sales_page = SalesPlanPage(logged_in)
        expected_url = f"{ERP_URL}{menu_urls['销售计划']}"

        # 导航到销售计划页面
        sales_page.navigate_to_sales_plan()

        logging.info("已导航到销售计划页面")

        # 获取实际页面URL（添加等待确保页面加载完成）
        current_url_all = logged_in.current_url
        current_url = current_url_all
        logging.info(f"实际页面URL: {current_url}")

        target_url = current_url_all
        logging.info(f"目标URL: {target_url}")


        # 对比URL时忽略末尾斜杠和大小写
        assert expected_url.lower().rstrip('/') == current_url.lower().rstrip('/'), \
            f"菜单跳转地址不正确\n预期: {expected_url}\n实际: {current_url}"


    def test_add_sales_plan_onemonth(self, logged_in, plan_data):
        """有效等价类：添加五月销售计划1000"""
        sales_plan_page = SalesPlanPage(logged_in)
        sales_plan_page.navigate_to_sales_plan()

        plan_data_item = plan_data[0]
        asin = plan_data_item['asin']
        
        success_message = sales_plan_page.add_sales_plan(asin=asin)
        logging.info(f"实际成功提示内容: {success_message}")
        try:
            # 验证成功消息
            assert "成功" in success_message, "提示消息应包含成功标识"
        except AssertionError as e:
            # 断言失败时记录日志并截图
            logging.error(f"断言失败: {str(e)}")
            sales_plan_page.take_screenshot('success_message_assertion_failed')
            raise

        # # 确保元素可点击
        # try:
        #     element = WebDriverWait(logged_in, 10).until(
        #         EC.element_to_be_clickable((By.ID, 'element_id'))  # 替换为实际的元素定位器
        #     )
        #     element.click()
        # except Exception as e:
        #     logging.error(f"元素点击失败: {str(e)}")
        #     sales_plan_page.take_screenshot('element_click_failed')
        #     raise

    def test_add_sales_plan_quantity(self, logged_in, plan_data):
        """测试计划数量"""
        
        sales_plan_page = SalesPlanPage(logged_in)
        sales_plan_page.navigate_to_sales_plan()

        plan_data_item = plan_data[0]
        asin = plan_data_item['asin']

        success_message = sales_plan_page.add_sales_plan(asin=asin)
        logging.info(f"实际成功提示内容: {success_message}")
        time.sleep(1)


        # 读取测试数据
        with open('d:/gmj/workSpaces/workSpaces_pycharm/autoTest4/TestCase/TestData/quantity_input.json', encoding='utf-8') as f:
            quantity_data = json.load(f)
        valid_cases = quantity_data.get('valid', [])
        invalid_cases = quantity_data.get('invalid', [])
        # 以“五月”为例，实际可参数化
        month_locator = elements_salesPlan.SalesPlanElements.SELECT_MONTH_5
        all_cases = valid_cases + invalid_cases
        results = sales_plan_page.add_sales_plan_with_quantity_cases(month_locator, all_cases)
        for r in results:
            print(f"输入: {r['input']}，期望: {r['expected']}，实际: {r['actual']}，结果: {r['result']}")
            # 可根据需要添加断言

    def test_add_sales_plan_sku(self, logged_in, plan_data):
        """测试sku"""


    def test_add_sales_plan_months(self, logged_in):
        """有效等价类，连续添加4个月的销售计划"""
        sales_plan_page = SalesPlanPage(logged_in)
        sales_plan_page.navigate_to_sales_plan()

        # 读取测试数据
        with open('d:/gmj/workSpaces/workSpaces_pycharm/autoTest4/TestCase/TestData/FBA_shipping.json', encoding='utf-8') as f:
            fba_shipping_data = json.load(f)

        for plan_data_item in fba_shipping_data:
            store = plan_data_item['store']
            marketplace = plan_data_item['marketplace']
            asin = plan_data_item['asin']
            months_data = plan_data_item['months']

            logging.info(f"开始为店铺: {store}, 市场: {marketplace}, ASIN: {asin} 添加销售计划")

            # 选择店铺和市场
            # sales_plan_page.select_store_and_market(store, marketplace)
            sales_plan_page.select_store_and_market()

            # 添加销售计划（ASIN）
            success_message = sales_plan_page.add_sales_plan(asin=asin)
            logging.info(f"ASIN添加成功提示: {success_message}")
            assert "成功" in success_message, f"ASIN {asin} 添加失败: {success_message}"

            # 连续添加多个月份的销售计划
            results = sales_plan_page.add_sales_plan_for_months(months_data)
            for r in results:
                logging.info(f"月份: {r['month']}，输入: {r['input']}，期望: {r['expected']}，实际: {r['actual']}，结果: {r['result']}")
                assert r['result'] == '成功', f"月份 {r['month']} 销售计划添加失败: {r['actual']}"


            # 循环取多个月份的计划数量
            for month_data in months_data:
                month = month_data['month']
                quantity = sales_plan_page.get_plan_quantity(month)
                logging.info(f"月份: {month}，计划数量: {quantity}")
                assert quantity == month_data['quantity'], f"月份 {month} 的计划数量错误，期望: {month_data['quantity']}，实际: {quantity}"

            logging.info(f"完成为店铺: {store}, 市场: {marketplace}, ASIN: {asin} 添加销售计划")
            # 可以添加一些清理或验证步骤，例如检查数据是否正确显示在页面上
