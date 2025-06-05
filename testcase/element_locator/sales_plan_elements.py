from selenium.webdriver.common.by import By

class SalesPlanElements:
    # 销售计划菜单
    # SALES_PLAN_MENU = (By.XPATH, "//span[text()='销售计划']")
    # SALES_PLAN_URL = "/salesplan/salesPlan/index"

    # 销售计划页面元素
    # ADD_SALES_PLAN_BUTTON = (By.XPATH, "//button/span[contains(text(),'创建需求')] ") # 创建需求按钮
    # MONTH_SELECT = (By.XPATH, "//input[@placeholder='请选择月份']") # 月份选择框
    # SELECT_MONTH_5 = (By.XPATH, "//li[text()='五月']") # 五月选项
    # PLAN_QUANTITY_INPUT = (By.XPATH, "//input[@placeholder='请输入计划数量']") # 计划数量输入框
    # SAVE_AND_CONTINUE_BUTTON = (By.XPATH, "//button/span[contains(text(),'保存并继续')] ") # 保存并继续按钮
    # CONFIRM_BUTTON = (By.XPATH, "//button/span[contains(text(),'确定')] ") # 确定按钮
    # SUCCESS_MESSAGE = (By.XPATH, "//p[text()='添加成功']") # 添加成功提示


    SALES_PLAN_URL = "/amzShipment/salesPlan"
    MENU_AMAZON = (By.XPATH, "//*[@role='menu']//span[text()='Amazon发货']")
    # SALES_PLAN_MENU = (By.XPATH,"//*[@role='menu']//a[@href='/amzShipment/salesPlan']")
    SALES_PLAN_MENU = (By.XPATH, "//*[@role='menu']//a[span[text()='销售计划']]")
    SEARCH_RESULT = (By.XPATH, "//div[contains(@class,'ant-table-body')]//tr")
    ADD_SALES_PLAN_BUTTON = (By.XPATH, "/html/body/div[1]/section/section/main/div[2]/div/div/div/div[3]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[17]/div/a")
    MONTH_SELECT = (By.XPATH, "//div[@class='ant-modal-content']//input[@placeholder='请选择月份']")
    # SELECT_MONTH_5 = (By.XPATH, "//a[@class='ant-calendar-month-panel-month' and text() = '五月']")
    SELECT_MONTH = (By.XPATH, "//a[@class='ant-calendar-month-panel-month' and text() = '五月']")
    PLAN_QUANTITY_INPUT = (By.XPATH, "//div[@class='ant-modal-content']//input[@placeholder='请输入计划数量']")
    SAVE_AND_CONTINUE_BUTTON = (By.XPATH,"//div[@class='ant-modal-footer']//button[@class='ant-btn ant-btn-primary']//span[text()='保存并继续']")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'确认')]")
    SUCCESS_MESSAGE = (By.XPATH, "//span[text()='添加成功！']")


    @staticmethod
    def get_month_locator(month):
        """根据月份名称返回对应的元素定位器"""
        return (By.XPATH, f"//a[@class='ant-calendar-month-panel-month' and text() = '{month}']")

    # 示例用法
    # month_locator = get_month_locator('六月')