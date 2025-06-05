# 分配订单
from selenium.webdriver.common.by import By

class AllocateOrderElements:
    ALLOCATE_ORDER_MENU = (By.XPATH, "//*[@role='menu']//a[span[text()='分配订单']]")

    PRODUCTION_DELIVERY_PLAN_NOT_GENERATED = (By.XPATH, "//div[@role='tab' and text()='待确认工厂']")
    PRODUCTION_DELIVERY_PLAN_GENERATED = (By.XPATH, "//div[@role='tab' and text()='已确认工厂']")