from selenium.webdriver.common.by import By

class SalesPlanElements:
    SALES_PLAN_URL = "/amzShipment/salesPlan"
    # AMAZON_MENU = (By.XPATH, "//*[@id='app']/section/aside/div/ul/li[3]/div/span/span")
    MENU_AMAZON = (By.XPATH, "//*[@role='menu']//span[text()='Amazon发货']")
    # SALES_PLAN_MENU = (By.CSS_SELECTOR, "#app > section > aside > div > ul > li.ant-menu-submenu.ant-menu-submenu-inline.ant-menu-submenu-open > ul > li:nth-child(2)")
    # SALES_PLAN_MENU = (By.XPATH,"//*[@role='menu']//span[text()='销售计划']")
    # SALES_PLAN_MENU = (By.XPATH,"//*[@role='menu']//a[@href='/amzShipment/salesPlan']/span[text()='销售计划']")
    SALES_PLAN_MENU = (By.XPATH,"//*[@role='menu']//a[@href='/amzShipment/salesPlan']")
    # 以下元素定位已迁移至BaseElement统一管理
    # ASIN_INPUT = (By.CSS_SELECTOR, "input[placeholder='请输入ASIN']")
    # STORE_LOCATOR = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[3]")
    # MARKET_LOCATOR = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[4]/div[1]/div[1]")
    # SEARCH_BUTTON = (By.XPATH, "//*[@id='app']/section/section/main/div[2]/div/div/div/div[2]/form/div/div[4]/span/button[1]")
    SEARCH_RESULT = (By.XPATH, "//div[contains(@class,'ant-table-body')]//tr")
    ADD_SALES_PLAN_BUTTON = (By.XPATH, "/html/body/div[1]/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[17]/div/a")
    MONTH_SELECT = (By.XPATH, "//div[@class='ant-modal-content']//input[@placeholder='请选择月份']")
    SELECT_MONTH_5 = (By.XPATH, "//a[@class='ant-calendar-month-panel-month' and text() = '五月']")
    PLAN_QUANTITY_INPUT = (By.XPATH, "//div[@class='ant-modal-content']//input[@placeholder='请输入计划数量']")
    SAVE_AND_CONTINUE_BUTTON = (By.XPATH,"//div[@class='ant-modal-footer']//button[@class='ant-btn ant-btn-primary']//span[text()='保存并继续']")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'确认')]")
    SUCCESS_MESSAGE = (By.XPATH, "/html/body/div[9]/span/div/div/div/span")