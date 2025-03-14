# testcase/test_sales_plan.py
from pages.sales_plan_page import SalesPlanPage
from selenium.webdriver.common.by import By


def test_menu_navigation(logged_in_driver, module_urls):
    """验证销售计划菜单跳转"""
    sales_page = SalesPlanPage(logged_in_driver)
    sales_page.navigate_to_sales_plan()
    
    assert logged_in_driver.current_url == module_urls["sales_plan"], "菜单跳转地址不正确"


def test_add_sales_plan(logged_in_driver):
    sales_plan_page = SalesPlanPage(logged_in_driver)
    asin = "your_asin"
    months = ["2024-01", "2024-02", "2024-03", "2024-04"]
    quantities = ["100", "200", "300", "400"]
    sales_plan_page.add_sales_plan(asin, months, quantities)

    # 假设成功提示信息的元素定位器
    SUCCESS_MESSAGE = (By.CSS_SELECTOR,'body > div.ant-notification.ant-notification-topRight > span > div > div > div > div.ant-notification-notice-message')
    try:
        success_message = sales_plan_page.find_element(*SUCCESS_MESSAGE)
        assert success_message.is_displayed()
        assert success_message.text == "销售计划添加成功"
    except Exception as e:
        assert False, f"添加销售计划失败: {e}"


def test_menu_structure(menu_urls):
    expected_urls = {
        "销售计划": "/erp/sale/sales-plan",
        "库存管理": "/erp/inventory/manage"
    }
    
    for name, url in expected_urls.items():
        assert name in menu_urls, f"缺少菜单项: {name}"
        assert menu_urls[name] == url, f"{name} URL不匹配"

