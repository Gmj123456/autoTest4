# 生产交付计划
from selenium.webdriver.common.by import By

class ProductionDeliveryPlanElements:
    PRODUCTION_DELIVERY_PLAN_MENU = (By.XPATH, "//*[@role='menu']//a[span[text()='交付计划']]")
    PRODUCTION_DELIVERY_PLAN_NOT_GENERATED = (By.XPATH, "//div[@role='tab' and text()='未生成生产交付计划']")
    PRODUCTION_DELIVERY_PLAN_GENERATED = (By.XPATH, "//div[@role='tab' and text()='已生成生产交付计划']")
    GENERATE_PRODUCTION_DELIVERY_BUTTON = (By.XPATH, "//button[contains(@class, 'ant-btn-primary') and span[text()='生成生产交付计划']]")
    # RECONFIRM_BUTTON = (By.XPATH, "//button[contains(@class, 'ant-btn ant-btn-primary') and span[normalize-space(text())='确定']]") # 三个确定按钮？
    RECONFIRM_BUTTON = (By.XPATH, "//div[contains(@class, 'ant-modal-confirm-btns')]//button[span[translate(text(), ' ', '')='确定']]")