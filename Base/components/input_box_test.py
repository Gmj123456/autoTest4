import json
import logging
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def load_test_data(json_path):
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)

class InputBoxTester:
    """
    通用输入框测试组件，支持单价和数量输入框的自动化测试。
    """
    def __init__(self, driver, input_locator, message_locator=None):
        self.driver = driver
        self.input_locator = input_locator
        self.message_locator = message_locator  # 用于获取错误提示信息

    def clear_and_input(self, value):
        input_box = self.driver.find_element(*self.input_locator)
        input_box.clear()
        input_box.send_keys(value)
        input_box.send_keys(Keys.TAB)  # 触发校验

    def get_message(self):
        if self.message_locator:
            try:
                return self.driver.find_element(*self.message_locator).text.strip()
            except NoSuchElementException:
                return ""
        return ""

    def get_value(self):
        return self.driver.find_element(*self.input_locator).get_attribute("value").strip()

    def run_test_cases(self, test_data):
        results = []
        for case in test_data["valid"]:
            self.clear_and_input(case["input"])
            actual_value = self.get_value()
            try:
                assert actual_value == case["expected"]["value"], f"期望值: {case['expected']['value']}，实际值: {actual_value}"
                results.append({"input": case["input"], "result": "通过", "actual": actual_value})
            except AssertionError as e:
                logging.error(f"有效用例失败: {case['input']} - {e}")
                results.append({"input": case["input"], "result": "失败", "error": str(e)})
        for case in test_data["invalid"]:
            self.clear_and_input(case["input"])
            actual_message = self.get_message()
            try:
                assert actual_message == case["expected"]["message"], f"期望提示: {case['expected']['message']}，实际提示: {actual_message}"
                results.append({"input": case["input"], "result": "通过", "actual": actual_message})
            except AssertionError as e:
                logging.error(f"无效用例失败: {case['input']} - {e}")
                results.append({"input": case["input"], "result": "失败", "error": str(e)})
        return results


def test_price_input(driver, input_locator, message_locator=None):
    """
    单价输入框通用测试方法
    :param driver: selenium webdriver实例
    :param input_locator: 输入框定位元组(By, value)
    :param message_locator: 错误提示定位元组(By, value)
    :return: 测试结果列表
    """
    data_path = os.path.join(os.path.dirname(__file__), '../../TestCase/TestData/price_input.json')
    test_data = load_test_data(os.path.abspath(data_path))
    tester = InputBoxTester(driver, input_locator, message_locator)
    return tester.run_test_cases(test_data)

def test_quantity_input(driver, input_locator, message_locator=None):
    """
    数量输入框通用测试方法
    :param driver: selenium webdriver实例
    :param input_locator: 输入框定位元组(By, value)
    :param message_locator: 错误提示定位元组(By, value)
    :return: 测试结果列表
    """
    data_path = os.path.join(os.path.dirname(__file__), '../../TestCase/TestData/quantity_input.json')
    test_data = load_test_data(os.path.abspath(data_path))
    tester = InputBoxTester(driver, input_locator, message_locator)
    return tester.run_test_cases(test_data)