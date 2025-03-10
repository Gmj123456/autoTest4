# pages/bak_login_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
# import utils.ocr as ocr  # 导入 ocr 模块
import time
from config.config import ERP_URL
from selenium.webdriver.common.keys import Keys  # 导入 Keys 类
import os

class LoginPage(BasePage):
    USERNAME_INPUT = (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[1]/div/div/span/input")
    PASSWORD_INPUT = (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[2]/div/div/span/input")
    CAPTCHA_INPUT = (By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[3]/div[1]/div/div/div/span/span/input")
    # LOGIN_BUTTON = (By.ID, "login-button")
    CAPTCHA_IMAGE = (By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[3]/div[2]/img")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.driver.get(ERP_URL)
        self.send_keys(*self.USERNAME_INPUT, username)
        self.send_keys(*self.PASSWORD_INPUT, password)

        # 截图验证码
        captcha_image = self.find_element(*self.CAPTCHA_IMAGE)
        captcha_image.screenshot("captcha.png")

        # 调用OCR接口识别验证码
        os_str = 'python ./utils/ocr.py'
        f = os.popen(os_str, 'r')
        res = f.readlines()
        f.close()

        # # 调用 OCR 接口识别验证码
        # self.send_keys(*self.CAPTCHA_INPUT, res + Keys.RETURN)  # 输入验证码后发送回车键
        self.send_keys(*self.CAPTCHA_INPUT, res)  # 输入验证码后发送回车键


        # # 调用 OCR 接口识别验证码
        # captcha_text = ocr.ocr_accurate_basic()
        # self.send_keys(*self.CAPTCHA_INPUT, captcha_text + Keys.RETURN)  # 输入验证码后发送回车键


        time.sleep(2)  # 等待登录完成