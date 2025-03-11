# pages/bak_login_page2.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time
from config.config import ERP_URL
from selenium.webdriver.common.keys import Keys
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LoginPage(BasePage):
    USERNAME_INPUT = (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[1]/div/div/span/input")
    PASSWORD_INPUT = (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[2]/div/div/span/input")
    CAPTCHA_INPUT = (By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[3]/div[1]/div/div/div/span/span/input")
    CAPTCHA_IMAGE = (By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[3]/div[2]/img")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            try:
                logging.info("开始登录操作")
                self.driver.get(ERP_URL)
                logging.info("已打开登录页面")
                self.send_keys(*self.USERNAME_INPUT, username)
                logging.info("已输入用户名")
                self.send_keys(*self.PASSWORD_INPUT, password)
                logging.info("已输入密码")

                # 获取当前脚本所在目录
                current_dir = os.path.dirname(os.path.abspath(__file__))
                # 构建保存图片的路径，保存到 config 文件夹
                config_dir = os.path.join(current_dir, '../config')
                if not os.path.exists(config_dir):
                    os.makedirs(config_dir)
                captcha_path = os.path.join(config_dir, 'captcha.png')

                try:
                    captcha_image = self.find_element(*self.CAPTCHA_IMAGE)
                    captcha_image.screenshot(captcha_path)
                except Exception as e:
                    print(f"截图验证码时出现异常: {e}")

                # 调用OCR接口识别验证码
                os_str = f'python {os.path.join(current_dir, "../utils/ocr.py")} {captcha_path}'
                # os_str = 'python ./utils/ocr.py'
                f = os.popen(os_str, 'r')
                res = f.readlines()
                f.close()

                if res:
                    captcha_text = res[0].strip()
                    self.send_keys(*self.CAPTCHA_INPUT, captcha_text + Keys.RETURN)
                    logging.info(f"已输入验证码: {captcha_text}，第 {attempts + 1} 次尝试")
                    time.sleep(2)  # 等待登录完成

                    # 假设成功提示信息的元素定位器
                    SUCCESS_MESSAGE = (By.CSS_SELECTOR,'body > div.ant-notification.ant-notification-topRight > span > div > div > div > div.ant-notification-notice-message')
                    try:
                        success_message = self.find_element(*SUCCESS_MESSAGE)
                        if success_message.is_displayed() and success_message.text == "登录成功":
                            logging.info("登录成功")
                            return True
                    except Exception:
                        pass

                attempts += 1
                logging.warning(f"第 {attempts} 次验证码识别失败，重新尝试")

            except Exception as e:
                logging.error(f"登录过程中出现错误: {e}")
                attempts += 1

        logging.error("验证码识别失败次数达到上限，登录失败")
        return False