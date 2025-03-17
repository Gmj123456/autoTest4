# pages/sales_plan_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SalesPlanPage(BasePage):
    AMAZON = (By.CSS_SELECTOR,"#app > section > aside > div > ul > li.ant-menu-submenu.ant-menu-submenu-inline.ant-menu-submenu-open > div > span > span")
    SALES_PLAN_MENU = (By.ID, "//*[@id='app']/section/aside/div/ul/li[3]/ul/li[2]/a/span")
    STORE_SELECT = (By.ID, "store-select")
    MARKET_SELECT = (By.ID, "market-select")
    ASIN_INPUT = (By.ID, "asin-input")
    SEARCH_BUTTON = (By.ID, "search-button")
    ADD_PLAN_BUTTON = (By.ID, "add-plan-button")
    MONTH_SELECT = (By.ID, "month-select")
    PLAN_QUANTITY_INPUT = (By.ID, "plan-quantity-input")
    CONFIRM_BUTTON = (By.ID, "confirm-button")
    
    # 新增定位器
    SALES_PLAN_URL = "/sales-plan"
    MONTH_LINK = (By.LINK_TEXT, "{}")  # 参数化定位器
    
    def add_single_plan(self, month: str, quantity: str):
        """添加单个销售计划"""
        self.click_element(*self.ADD_PLAN_BUTTON)
        
        # 带参数的定位器使用
        month_locator = (self.MONTH_LINK[0], self.MONTH_LINK[1].format(month))
        self.click_element(*month_locator)
        
        self.send_keys(*self.PLAN_QUANTITY_INPUT, quantity)
        self.click_element(*self.CONFIRM_BUTTON)

    def __init__(self, driver):
        super().__init__(driver)

    def add_sales_plan(self, asin, months, quantities):
        self.click_element(*self.SALES_PLAN_MENU)
        self.click_element(*self.STORE_SELECT)  # 选择店铺
        self.click_element(*self.MARKET_SELECT)  # 选择市场
        self.send_keys(*self.ASIN_INPUT, asin)
        self.click_element(*self.SEARCH_BUTTON)

        for month, quantity in zip(months, quantities):
            self.click_element(*self.ADD_PLAN_BUTTON)
            self.send_keys(*self.MONTH_SELECT, month)
            self.send_keys(*self.PLAN_QUANTITY_INPUT, quantity)

        self.click_element(*self.CONFIRM_BUTTON)
    
    def navigate_to_sales_plan(self):
        """导航到销售计划页面"""
        self.click_element(*self.SALES_PLAN_MENU)
        # 添加显式等待确保页面加载完成
        WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url.endswith('/sales-plan') or d.current_url.endswith('/salesPlan')
        )
    
    def get_current_url(self):
        """获取当前页面URL"""
        return self.driver.current_url
