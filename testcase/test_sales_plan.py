# autoTest1/TestCase/test_sales_plan.py
import pytest
from Base.base_page import BasePage
from Base.config import ERP_URL
from PageObject.sales_plan_page import SalesPlanPage
import logging
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestCase.conftest import logged_in

"""
1. 销售计划
2. 
"""
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


    def test_add_sales_plan(self, logged_in, plan_data):
        """有效等价类：添加销售计划"""

        sales_plan_page = SalesPlanPage(logged_in)
        sales_plan_page.navigate_to_sales_plan()

        plan_data_item = plan_data[0]
        asin = plan_data_item['asin']
        
        sales_plan_page.add_sales_plan(asin=asin)
        
        try:
            assert sales_plan_page.is_success_message_displayed(), "应显示成功提示"
            success_message = sales_plan_page.find_element(*sales_plan_page.SUCCESS_MESSAGE).text
            logging.info(f"实际成功提示内容: {success_message}")
            assert "成功" in success_message, "提示消息应包含成功标识"
        except AssertionError as e:
            sales_plan_page.take_screenshot('assert_failure')
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            screenshot_dir = os.path.join(os.path.dirname(__file__), '../screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            source_path = os.path.join(screenshot_dir, f'assert_failure_{timestamp}.html')
            with open(source_path, 'w', encoding='utf-8') as f:
                f.write(logged_in.page_source)
            logging.error(f"断言失败，页面源码已保存至：{source_path}")
            raise
        #     assert logged_in.current_url == sales_plan_page.SALES_PLAN_URL, "应在销售计划页面"
        # except AssertionError as e:
        #     # 调用截图方法
        #     sales_plan_page.take_screenshot('assert_failure')
        #     # 保存页面源码到文件
        #     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        #     screenshot_dir = os.path.join(os.path.dirname(__file__), '../screenshots')
        #     os.makedirs(screenshot_dir, exist_ok=True)
        #     source_path = os.path.join(screenshot_dir, f'assert_failure_{timestamp}.html')
        #     with open(source_path, 'w', encoding='utf-8') as f:
        #         f.write(logged_in.page_source)
        #     logging.error(f"断言失败，页面源码已保存至：{source_path}")
        #     raise
        # # 新增：验证搜索结果区域存在（补充检查）
        # assert len(logged_in.find_elements(*SalesPlanPage.SEARCH_RESULT)) > 0, "搜索结果区域未加载"