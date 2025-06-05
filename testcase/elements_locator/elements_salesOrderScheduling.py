# 销售排单

from selenium.webdriver.common.by import By

class SalesOrderSchedulingElements:
    SALES_ORDER_SCHEDULING_MENU = (By.XPATH, "//*[@role='menu']//a[span[text()='销售排单']]")
    PENDING_ORDER_SCHEDULING = (By.XPATH,"//div[@role='tab' and text()='待排单']")
    SCHEDULED_ORDER = (By.XPATH,"//div[@role='tab' and text()='已排单']")
    GENERATE_SCHEDULING_TABLE_BUTTON = (By.XPATH,"//button[contains(@class, 'ant-btn-primary') and span[text()='生成排单表']]")
    ALL_ASINS = (By.XPATH, "//li[normalize-space(text())='全部ASIN']")  # 全部ASIN，使用normalize-space()去除前后空格
    CUSTOM_ASINS = (By.XPATH, "//li[normalize-space(text())='自定义ASIN']")  # 自定义ASIN
    SALES_DEMAND_ASINS = (By.XPATH, "//li[normalize-space(text())='销售需求ASIN']")  # 销售需求ASIN