from selenium.webdriver.common.by import By

class SalesPlanElements:
    SALES_PLAN_URL = "/amzShipment/salesPlan"
    MENU_AMAZON = (By.XPATH, "//*[@role='menu']//span[text()='Amazon发货']")
    SALES_PLAN_MENU = (By.XPATH,"//*[@role='menu']//a[@href='/amzShipment/salesPlan']")
    SEARCH_RESULT = (By.XPATH, "//div[contains(@class,'ant-table-body')]//tr")
    ADD_SALES_PLAN_BUTTON = (By.XPATH, "/html/body/div[1]/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[17]/div/a")
    MONTH_SELECT = (By.XPATH, "//div[@class='ant-modal-content']//input[@placeholder='请选择月份']")
    SELECT_MONTH_5 = (By.XPATH, "//a[@class='ant-calendar-month-panel-month' and text() = '五月']")
    PLAN_QUANTITY_INPUT = (By.XPATH, "//div[@class='ant-modal-content']//input[@placeholder='请输入计划数量']")
    SAVE_AND_CONTINUE_BUTTON = (By.XPATH,"//div[@class='ant-modal-footer']//button[@class='ant-btn ant-btn-primary']//span[text()='保存并继续']")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'确认')]")
    SUCCESS_MESSAGE = (By.XPATH, "//span[text()='添加成功！']")