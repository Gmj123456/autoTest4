# pages/base_page.py
import os
import logging
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException
import json
import time


class BasePage:
    """
    页面基类，提供通用的页面操作方法
    """
    # 默认配置常量
    DEFAULT_TIMEOUT = 15
    DEFAULT_POLL_FREQUENCY = 0.5
    SCREENSHOT_DIR = '../screenshots'
    
    def __init__(self, driver, timeout=None):
        """
        初始化页面基类
        :param driver: WebDriver实例
        :param timeout: 默认超时时间（秒）
        """
        self.driver = driver
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.wait = WebDriverWait(self.driver, self.timeout, self.DEFAULT_POLL_FREQUENCY)
        self.actions = ActionChains(self.driver)

    def navigate_to_menu(self, menu_locator, submenu_locator=None, url_keyword=None, timeout=None):
        """
        通用菜单导航方法
        :param menu_locator: 主菜单定位元组 (By, value)
        :param submenu_locator: 子菜单定位元组（可选）
        :param url_keyword: URL中应包含的关键字（可选）
        :param timeout: 超时时间（可选）
        :return: 导航是否成功
        """
        timeout = timeout or self.timeout
        try:
            logging.info(f"开始导航菜单 - 主菜单: {menu_locator}")
            
            # 点击主菜单
            main_menu = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(menu_locator)
            )
            self._safe_click(main_menu)
            logging.info("主菜单点击成功")
            
            # 点击子菜单（如果存在）
            if submenu_locator:
                logging.info(f"点击子菜单: {submenu_locator}")
                submenu = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(submenu_locator)
                )
                self._safe_click(submenu)
                logging.info("子菜单点击成功")
            
            # 等待URL变化（如果指定）
            if url_keyword:
                logging.info(f"等待URL包含关键字: {url_keyword}")
                WebDriverWait(self.driver, timeout).until(
                    EC.url_contains(url_keyword)
                )
                logging.info(f"URL已包含关键字: {url_keyword}")
            
            return True
            
        except TimeoutException as e:
            error_msg = f"菜单导航超时: {str(e)}"
            logging.error(error_msg)
            self.take_screenshot("menu_navigation_timeout")
            raise TimeoutException(error_msg)
        except Exception as e:
            error_msg = f"导航菜单异常: {str(e)}"
            logging.error(error_msg)
            self.take_screenshot("menu_navigation_error")
            raise

    def select_store_and_market(self):
        """选择店铺和市场"""
        try:
            from Base.base_element import BaseElement
            logging.info("开始选择店铺和市场")
            
            logging.info("点击店铺选择器")
            self.click_element(*BaseElement.STORE_LOCATOR)
            
            logging.info("点击市场选择器")
            self.click_element(*BaseElement.MARKET_LOCATOR)
            
            logging.info("店铺和市场选择完成")
            
        except Exception as e:
            error_msg = f"选择店铺或市场失败: {str(e)}"
            logging.error(error_msg)
            self.take_screenshot("select_store_market_error")
            raise

    def find_element(self, by, value, timeout=None, condition=None):
        """
        查找元素的通用方法
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        :param condition: 等待条件，默认为element_to_be_clickable
        :return: WebElement
        """
        timeout = timeout or self.timeout
        condition = condition or EC.element_to_be_clickable
        
        try:
            return WebDriverWait(self.driver, timeout).until(
                condition((by, value))
            )
        except TimeoutException as e:
            error_msg = f"查找元素超时: {by}={value}"
            logging.error(error_msg)
            self.take_screenshot("find_element_timeout")
            raise TimeoutException(error_msg)

    def find_elements(self, by, value, timeout=None):
        """
        查找多个元素
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        :return: List[WebElement]
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return self.driver.find_elements(by, value)
        except TimeoutException:
            logging.warning(f"未找到元素: {by}={value}")
            return []

    def click_element(self, by, value, timeout=None):
        """
        点击元素的通用方法
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            self._safe_click(element)
            logging.info(f"成功点击元素: {by}={value}")
            
        except TimeoutException as e:
            error_msg = f"点击元素超时: {by}={value}"
            logging.error(error_msg)
            self.take_screenshot("click_element_timeout")
            raise TimeoutException(error_msg)
        except Exception as e:
            error_msg = f"点击元素异常: {by}={value}, 错误: {str(e)}"
            logging.error(error_msg)
            self.take_screenshot("click_element_error")
            raise

    def _safe_click(self, element):
        """
        安全点击方法，包含多种点击策略
        :param element: WebElement
        """
        try:
            # 策略1: 普通点击
            element.click()
        except ElementNotInteractableException:
            try:
                # 策略2: 滚动到元素后点击
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.click()
            except Exception:
                # 策略3: JavaScript点击
                self.driver.execute_script("arguments[0].click();", element)
                logging.info("使用JavaScript点击元素")

    def send_keys(self, by, value, text, timeout=None, clear_first=True):
        """
        输入文本的通用方法
        :param by: 定位方式
        :param value: 定位值
        :param text: 要输入的文本
        :param timeout: 超时时间
        :param clear_first: 是否先清空输入框
        """
        timeout = timeout or self.timeout
        try:
            element = self.find_element(by, value, timeout)
            
            if clear_first:
                self._clear_input(element)
            
            element.send_keys(text)
            logging.info(f"成功输入文本到元素: {by}={value}")
            
        except Exception as e:
            error_msg = f"输入文本异常: {by}={value}, 错误: {str(e)}"
            logging.error(error_msg)
            self.take_screenshot("send_keys_error")
            raise

    def _clear_input(self, element):
        """
        清空输入框的多种策略
        :param element: WebElement
        """
        try:
            # 策略1: 标准清空
            element.clear()
        except Exception:
            try:
                # 策略2: 键盘操作清空
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.DELETE)
            except Exception:
                # 策略3: JavaScript清空
                self.driver.execute_script("arguments[0].value = '';", element)

    def wait_for_element_visibility(self, by, value, timeout=None):
        """
        等待元素可见
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        :return: WebElement
        """
        timeout = timeout or self.timeout
        return self.find_element(by, value, timeout, EC.visibility_of_element_located)

    def wait_for_element_invisible(self, by, value, timeout=None):
        """
        等待元素不可见
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        :return: bool
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
        except TimeoutException:
            return False

    def wait_for_text_in_element(self, by, value, text, timeout=None):
        """
        等待元素包含指定文本
        :param by: 定位方式
        :param value: 定位值
        :param text: 期望的文本
        :param timeout: 超时时间
        :return: bool
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, value), text)
            )
        except TimeoutException:
            return False

    def get_element_text(self, by, value, timeout=None):
        """
        获取元素文本
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        :return: str
        """
        try:
            element = self.wait_for_element_visibility(by, value, timeout)
            return element.text.strip()
        except Exception as e:
            logging.error(f"获取元素文本失败: {by}={value}, 错误: {str(e)}")
            return ""

    def get_element_attribute(self, by, value, attribute, timeout=None):
        """
        获取元素属性
        :param by: 定位方式
        :param value: 定位值
        :param attribute: 属性名
        :param timeout: 超时时间
        :return: str
        """
        try:
            element = self.find_element(by, value, timeout)
            return element.get_attribute(attribute)
        except Exception as e:
            logging.error(f"获取元素属性失败: {by}={value}, 属性: {attribute}, 错误: {str(e)}")
            return ""

    def is_element_present(self, by, value, timeout=3):
        """
        检查元素是否存在
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        :return: bool
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, by, value, timeout=3):
        """
        检查元素是否可见
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        :return: bool
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, by, value, timeout=None):
        """
        滚动到指定元素
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        """
        try:
            element = self.find_element(by, value, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # 等待滚动完成
        except Exception as e:
            logging.error(f"滚动到元素失败: {by}={value}, 错误: {str(e)}")

    def hover_over_element(self, by, value, timeout=None):
        """
        鼠标悬停在元素上
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 超时时间
        """
        try:
            element = self.find_element(by, value, timeout)
            self.actions.move_to_element(element).perform()
            logging.info(f"鼠标悬停在元素上: {by}={value}")
        except Exception as e:
            logging.error(f"鼠标悬停失败: {by}={value}, 错误: {str(e)}")

    def take_screenshot(self, filename_prefix="screenshot"):
        """
        截取当前页面截图并保存
        :param filename_prefix: 文件名前缀
        :return: 截图文件路径
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        screenshot_dir = os.path.join(os.path.dirname(__file__), self.SCREENSHOT_DIR)
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f'{filename_prefix}_{timestamp}.png')
        
        try:
            self.driver.save_screenshot(screenshot_path)
            logging.info(f"截图已保存至：{screenshot_path}")
            return screenshot_path
        except Exception as e:
            logging.error(f"截图失败: {str(e)}")
            return None

    def wait_for_page_load(self, timeout=None):
        """
        等待页面加载完成
        :param timeout: 超时时间
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logging.info("页面加载完成")
        except TimeoutException:
            logging.warning("页面加载超时")

    def refresh_page(self):
        """刷新当前页面"""
        try:
            self.driver.refresh()
            self.wait_for_page_load()
            logging.info("页面刷新完成")
        except Exception as e:
            logging.error(f"页面刷新失败: {str(e)}")

    def get_current_url(self):
        """获取当前页面URL"""
        return self.driver.current_url

    def get_page_title(self):
        """获取页面标题"""
        return self.driver.title

    def load_test_data(self, file_path, min_version='1.0'):
        """
        通用测试数据加载方法
        :param file_path: 测试数据文件路径
        :param min_version: 最小版本要求
        :return: 测试数据字典
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"测试数据文件不存在: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 数据格式验证
            if not isinstance(data, list) or len(data) < 1:
                raise ValueError("测试数据格式错误，应为非空数组")
            
            # 版本检查
            if 'data_version' not in data[0]:
                logging.warning("测试数据缺少版本信息")
            elif data[0]['data_version'] < min_version:
                raise ValueError(f"数据版本过低，当前版本: {data[0]['data_version']}, 最低要求版本: {min_version}")
            
            logging.info(f"成功加载测试数据: {file_path}")
            return data[0]
            
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            error_msg = f"加载测试数据失败: {str(e)}"
            logging.error(error_msg)
            self.take_screenshot(f"load_data_error")
            raise Exception(error_msg)

    def execute_javascript(self, script, *args):
        """
        执行JavaScript代码
        :param script: JavaScript代码
        :param args: 参数
        :return: 执行结果
        """
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logging.error(f"执行JavaScript失败: {str(e)}")
            raise

    def switch_to_frame(self, frame_locator):
        """
        切换到指定frame
        :param frame_locator: frame定位器
        """
        try:
            if isinstance(frame_locator, tuple):
                frame = self.find_element(*frame_locator)
            else:
                frame = frame_locator
            self.driver.switch_to.frame(frame)
            logging.info("成功切换到frame")
        except Exception as e:
            logging.error(f"切换frame失败: {str(e)}")
            raise

    def switch_to_default_content(self):
        """切换回默认内容"""
        try:
            self.driver.switch_to.default_content()
            logging.info("成功切换回默认内容")
        except Exception as e:
            logging.error(f"切换回默认内容失败: {str(e)}")

    def close_current_window(self):
        """关闭当前窗口"""
        try:
            self.driver.close()
            logging.info("当前窗口已关闭")
        except Exception as e:
            logging.error(f"关闭窗口失败: {str(e)}")

    def switch_to_window(self, window_handle):
        """
        切换到指定窗口
        :param window_handle: 窗口句柄
        """
        try:
            self.driver.switch_to.window(window_handle)
            logging.info(f"成功切换到窗口: {window_handle}")
        except Exception as e:
            logging.error(f"切换窗口失败: {str(e)}")
            raise

    def get_window_handles(self):
        """获取所有窗口句柄"""
        return self.driver.window_handles

    def __del__(self):
        """析构函数，清理资源"""
        try:
            if hasattr(self, 'driver') and self.driver:
                # 可以在这里添加清理逻辑
                pass
        except Exception:
            pass

