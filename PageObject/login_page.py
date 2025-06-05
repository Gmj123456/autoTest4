import json
import logging
from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from Base.config import ERP_URL, LOGIN_SUCCESS_URL
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import subprocess
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestCase.elements_locator.elements_login import LoginElements

# 在文件顶部添加统一日志配置
from Base.utils.logger import setup_logging
setup_logging()

class LoginPage(BasePage):
   
    def __init__(self, driver):
        super().__init__(driver)
        # 确保 self.driver 是正确的驱动对象
        self.driver = driver

    def save_captcha_image(self):
        """保存验证码图片"""
        current_dir = Path(__file__).parent.resolve()
        captcha_dir = current_dir.parent /'Base' / 'utils'
        captcha_dir.mkdir(parents=True, exist_ok=True)
        captcha_path = captcha_dir / 'captcha.png'

        try:
            captcha_image = self.find_element(*LoginElements.CAPTCHA_IMAGE)
            captcha_image.screenshot(str(captcha_path))
            logging.info(f"验证码图片已保存到 {captcha_path}")
            return captcha_path
        except NoSuchElementException:
            logging.error("未找到验证码图片元素")
        except WebDriverException as e:
            logging.error(f"截图验证码时出现 WebDriver 异常: {e}")
        return None

    def recognize_captcha(self, captcha_path):
        """调用 OCR 接口识别验证码"""
        if not captcha_path:
            return None
        current_dir = Path(__file__).parent.resolve() 
        ocr_script_path = current_dir.parent /'Base' / 'utils' / 'ocr.py'

        try:
            # 检查 OCR 脚本文件是否存在
            if not ocr_script_path.exists():
                logging.error(f"OCR 脚本文件不存在: {ocr_script_path}")
                return None

            # 添加工作目录参数
            result = subprocess.run(
                ['python', str(ocr_script_path), str(captcha_path)], 
                cwd=str(Path(__file__).parent.parent.parent),  # 设置工作目录为项目根目录
                capture_output=True, 
                text=True,
                check=True
            )
            res = result.stdout.splitlines()
            if res:
                captcha_text = res[0].strip()
                logging.info(f"验证码识别结果: {captcha_text}")
                return captcha_text
        except subprocess.CalledProcessError as e:
            logging.error(f"调用 OCR 脚本时出现错误: {e.stderr}")
        except Exception as e:
            logging.error(f"识别验证码时出现未知错误: {e}")
        return None

    def check_login_result(self, attempts):
        """检查登录结果，等待页面 URL 变为登录成功后的 URL，最多等待 5 秒"""
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.current_url == LOGIN_SUCCESS_URL)
            logging.info("登录成功")
            return True
        except Exception:
            logging.warning(f"第 {attempts + 1} 次登录失败，重新尝试")
            return False

    # def get_access_token_ptuser(self):
    #     """获取并解析token"""
    #     try:
    #         # 等待页面加载完成（根据实际情况调整等待条件）
    #         WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    #         # 获取localStorage中的所有数据
    #         localStorage = self.driver.execute_script('return window.localStorage;')
    #         # 尝试从 localStorage 中获取 pro__Access-Token 的值
    #         access_token_str = localStorage.get('pro__Access-Token')
    #         if access_token_str:
    #             try:
    #                 # 将获取到的字符串解析为 Python 字典
    #                 access_token_dict = json.loads(access_token_str)
    #                 # 从字典中提取 "value" 键对应的值
    #                 value = access_token_dict.get("value")
    #                 if value:
    #                     logging.info(f"Token: {value}")
    #                     return value
    #                 else:
    #                     logging.error("pro__Access-Token 中不存在 value 字段")
    #             except json.JSONDecodeError:
    #                 logging.error("无法将 pro__Access-Token 的值解析为 JSON 格式")
    #         else:
    #             # 如果未找到 pro__Access-Token，打印提示信息
    #             logging.error("未找到 pro__Access-Token")
    #     except Exception as e:
    #         logging.error(f"An error occurred: {e}")
    #     return None

    def close_notification_box(self, NOTIFICATION_CLOSE_BUTTON=None):
        """关闭通知框"""
        try:
            # 检查通知框是否存在
            if NOTIFICATION_CLOSE_BUTTON:
                self.find_element(*NOTIFICATION_CLOSE_BUTTON).click()
                logging.info("已关闭通知框")
        except Exception as e:
            logging.error(f"没有通知框遮挡: {e}")

    def login(self, username, password):
        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            try:
                logging.info("开始登录操作")
                self.driver.get(ERP_URL)
                logging.info("已打开登录页面")
                self.send_keys(*LoginElements.USERNAME_INPUT, username)
                logging.info(f"已输入用户名：{username}")
                self.send_keys(*LoginElements.PASSWORD_INPUT, password)
                logging.info(f"已输入密码：{password}")

                captcha_path = self.save_captcha_image()
                captcha_text = self.recognize_captcha(captcha_path)

                print(captcha_text)

                if captcha_text:
                    self.send_keys(*LoginElements.CAPTCHA_INPUT, captcha_text + Keys.RETURN)
                    logging.info(f"已输入验证码: {captcha_text}，第 {attempts + 1} 次尝试")
                    result = self.check_login_result(attempts)
                    if result:
                        # self.access_token_ptuser = self.get_access_token_ptuser()  # 获取token
                        return True
            except Exception as e:
                logging.error(f"登录过程中出现错误: {str(e)}", exc_info=True)

            attempts += 1

        logging.error("验证码识别失败次数达到上限，登录失败")
        return False

    def logout(self):
        try:
            # 加强通知框关闭逻辑
            self.close_notification_box(LoginElements.NOTIFICATION_CLOSE_BUTTON)  # 明确传入定位器
            
            # 使用显式等待确保元素可点击
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # 等待退出按钮可点击
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LoginElements.LOGOUT_BUTTON)
            )
            logout_button.click()
            logging.info("已点击退出登录按钮")
        
            # 增加弹窗消失等待
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(LoginElements.NOTIFICATION_CLOSE_BUTTON)
            )
        
            # 优化确认按钮定位和等待策略
            try:
                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(LoginElements.CONFIRM_LOGOUT_BUTTON)
                )
                confirm_button.click()
                logging.info("已点击确定按钮，完成退出登录")
                
                # 新增等待页面跳转
                WebDriverWait(self.driver, 10).until(
                    EC.url_contains("login")
                )
                
            except Exception as e:
                logging.error(f"确认退出操作失败: {e}")
                return False

            return True
        except Exception as e:
            logging.error(f"退出登录时出现错误: {e}")
            return False
