# autoTest1/testcase/test_sales_plan.py
import pytest

from config.config import ERP_URL
from element_location.save_html import save_body_content_to_file
from element_location.kimi_upload_files import analyze_html_for_testing
from pages.sales_plan_page import SalesPlanPage
from selenium.webdriver.common.by import By
from pathlib import Path
import json
import logging

from testcase.conftest import logged_in


class TestSalesPlan:

    def test_save_authorized_pages(self, logged_in):
        """验证页面html保存功能"""
        url = r"http://192.168.150.222:3066/amzShipment/salesPlan"
        output_file = "salesPlan.html"
        
        save_body_content_to_file(logged_in, url, file=output_file)
        
        # 验证文件保存结果
        saved_path = Path(output_file)
        assert saved_path.exists(), f"文件{saved_path}未成功生成"
        assert saved_path.stat().st_size > 0, "保存的文件内容为空"
   

    def test_upload_files(self):
        """测试文件上传功能"""
        from element_location.kimi_upload_files import analyze_html_for_testing
    
        # 使用实际保存的HTML文件
        test_html = "html_output/amzShipment_salesPlan.html"
        output_json = "sales_plan_element_location.json"
    
        # 生成元素定位文件
        analyze_html_for_testing(html_file_path=test_html, ele_loc_file=output_json)

    def test_menu_navigation(self, logged_in, menu_urls):
        """验证销售计划菜单跳转"""
        # 添加空值检查
        assert menu_urls is not None, "菜单URL数据未正确加载"
        assert "销售计划" in menu_urls, "菜单数据中缺少销售计划项"

        sales_page = SalesPlanPage(logged_in)
        expected_url = menu_urls["销售计划"]

        # 导航到销售计划页面
        sales_page.navigate_to_sales_plan()

        # 获取实际页面URL（添加等待确保页面加载完成）
        current_url_all = logged_in.current_url
        current_url = current_url_all.replace(ERP_URL, "")

        print(current_url)
        logging.info(current_url)

        target_url = current_url_all

        # 调用修改后的 save_body_content_to_file 函数，传入 driver 和 url
        save_body_content_to_file(logged_in, target_url, file_path='sales_plan_body.html')

        analyze_html_for_testing(html_file_path='sales_plan_body.html', ele_loc_file='sales_plan_element_location.json')

        # 对比URL时忽略末尾斜杠和大小写
        assert expected_url.lower().rstrip('/') == current_url.lower().rstrip('/'), \
            f"菜单跳转地址不正确\n预期: {expected_url}\n实际: {current_url}"

    # 新增测试数据加载
    TEST_DATA_PATH = Path(__file__).parent.parent / 'testdata' / 'sales_plan_data.json'

    # 新增参数化测试用例
    @pytest.mark.parametrize('plan_data',
                             json.loads(TEST_DATA_PATH.read_text(encoding='utf-8')),
                             ids=lambda d: f"添加{d['month']}计划")
    def test_add_sales_plan(self, logged_in, plan_data):
        """集成后的销售计划添加测试（参数化版本）"""
        sales_plan_page = SalesPlanPage(logged_in)
        sales_plan_page.navigate_to_sales_plan()

        # 使用页面对象方法
        sales_plan_page.add_single_plan(
            month=plan_data['month'],
            quantity=plan_data['value']
        )

        # 验证结果
        assert sales_plan_page.is_success_message_displayed(), "应显示成功提示"
        assert sales_plan_page.get_current_url() == sales_plan_page.SALES_PLAN_URL, "应在销售计划页面"