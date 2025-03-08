# pages/login_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import utils.ocr as ocr
import time

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    CAPTCHA_INPUT = (By.ID, "captcha")
    LOGIN_BUTTON = (By.ID, "login-button")
    CAPTCHA_IMAGE = (By.ID, "captcha-image")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.driver.get(ERP_URL)
        self.send_keys(*self.USERNAME_INPUT, username)
        self.send_keys(*self.PASSWORD_INPUT, password)

        # 截图验证码
        captcha_image = self.find_element(*self.CAPTCHA_IMAGE)
        captcha_image.screenshot("captcha.png")

        # 调用 OCR 接口识别验证码
        captcha_text = ocr.recognize_captcha("captcha.png")
        self.send_keys(*self.CAPTCHA_INPUT, captcha_text)

        self.click_element(*self.LOGIN_BUTTON)
        time.sleep(2)  # 等待登录完成