# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def click_element(self, by, value, timeout=10):
        element = self.find_element(by, value, timeout)
        element.click()

    def send_keys(self, by, value, text, timeout=10):
        element = self.find_element(by, value, timeout)
        element.clear()
        element.send_keys(text)

    def get_locator_by_text(self, json_file, target_text):
        """
        根据文本从 JSON 文件中获取定位器
        参数:
            json_file: JSON 文件路径
            target_text: 要匹配的文本
            
        返回:
            匹配的定位器值，如果未找到则返回 None
        """
        import json
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 遍历 tabs 模块
            if 'tabs_module' in data:
                for tab in data['tabs_module']['tabs']:
                    if tab.get('text') == target_text:
                        return (tab['locator'], tab['value'])
            
            # 遍历 form_buttons 模块
            if 'search_module' in data and 'form_buttons' in data['search_module']:
                for button in data['search_module']['form_buttons']:
                    if button.get('text') == target_text:
                        return (button['locator'], button['value'])
            
            # 遍历 table_headers 模块
            if 'table_module' in data and 'table_headers' in data['table_module']:
                for header in data['table_module']['table_headers']:
                    if header.get('text') == target_text:
                        return (header['locator'], header['value'])
            
            # 遍历 pagination_buttons 模块
            if 'pagination_module' in data and 'pagination_buttons' in data['pagination_module']:
                for button in data['pagination_module']['pagination_buttons']:
                    if button.get('text') == target_text:
                        return (button['locator'], button['value'])
            
        except Exception as e:
            logging.error(f"从 JSON 文件获取定位器时出错: {e}")
        
        return None