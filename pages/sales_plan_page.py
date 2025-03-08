# pages/sales_plan_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SalesPlanPage(BasePage):
    SALES_PLAN_MENU = (By.ID, "sales-plan-menu")
    STORE_SELECT = (By.ID, "store-select")
    MARKET_SELECT = (By.ID, "market-select")
    ASIN_INPUT = (By.ID, "asin-input")
    SEARCH_BUTTON = (By.ID, "search-button")
    ADD_PLAN_BUTTON = (By.ID, "add-plan-button")
    MONTH_SELECT = (By.ID, "month-select")
    PLAN_QUANTITY_INPUT = (By.ID, "plan-quantity-input")
    CONFIRM_BUTTON = (By.ID, "confirm-button")

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