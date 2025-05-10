# autoTest1/TestCase/test_sales_plan.py
import pytest
from Base.base_page import BasePage
from Base.config import ERP_URL
from PageObject.sales_plan_page import SalesPlanPage
import logging
from selenium.webdriver.support.ui import WebDriverWait
from TestCase.conftest import logged_in

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
        expected_url = menu_urls["销售计划"]

        # 导航到销售计划页面
        sales_page.navigate_to_sales_plan()

        logging.info("已导航到销售计划页面")

        # 获取实际页面URL（添加等待确保页面加载完成）
        current_url_all = logged_in.current_url
        # current_url = current_url_all.replace(ERP_URL, "")
        current_url = current_url_all
        logging.info(f"实际页面URL: {current_url}")

        target_url = current_url_all
        logging.info(f"目标URL: {target_url}")


        # 对比URL时忽略末尾斜杠和大小写
        assert expected_url.lower().rstrip('/') == current_url.lower().rstrip('/'), \
            f"菜单跳转地址不正确\n预期: {expected_url}\n实际: {current_url}"


    def test_add_sales_plan(self, logged_in, plan_data):
        """集成后的销售计划添加测试（参数化版本）"""
        sales_plan_page = SalesPlanPage(logged_in)
        sales_plan_page.navigate_to_sales_plan()

        # 使用页面对象方法
        sales_plan_page.add_single_plan(
            asin=plan_data['asin'],
            months=plan_data['months'],
            quantities=plan_data['quantities']
        )

        # 验证结果
        assert sales_plan_page.is_success_message_displayed(), "应显示成功提示"
        assert sales_plan_page.get_current_url() == sales_plan_page.SALES_PLAN_URL, "应在销售计划页面"