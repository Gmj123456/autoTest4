import pytest
from unittest.mock import MagicMock, patch
from pages.login_page import LoginPage
import json

@pytest.fixture
def mock_driver():
    driver = MagicMock()
    # 模拟 localStorage 数据
    mock_localstorage = {
        'pro__Access-Token': json.dumps({"value": "mock_token_123"})
    }
    driver.execute_script.return_value = mock_localstorage
    return driver

def test_get_access_token_success(mock_driver):
    """测试成功获取token的情况"""
    # 模拟页面元素加载
    mock_driver.find_element.return_value = MagicMock()
    
    login_page = LoginPage(mock_driver)
    token = login_page.get_access_token()
    
    assert token == "mock_token_123"
    mock_driver.execute_script.assert_called_with('return window.localStorage;')

def test_get_access_token_missing_key(mock_driver):
    """测试缺少pro__Access-Token的情况"""
    mock_driver.execute_script.return_value = {}
    login_page = LoginPage(mock_driver)
    
    token = login_page.get_access_token()
    
    assert token is None

def test_get_access_token_invalid_json(mock_driver):
    """测试无效JSON数据的情况"""
    # 模拟无效的JSON字符串
    mock_driver.execute_script.return_value = {'pro__Access-Token': 'invalid_json'}
    login_page = LoginPage(mock_driver)
    
    token = login_page.get_access_token()
    
    assert token is None

def test_get_access_token_missing_value(mock_driver):
    """测试缺少value字段的情况"""
    mock_driver.execute_script.return_value = {
        'pro__Access-Token': json.dumps({"other_key": "value"})
    }
    login_page = LoginPage(mock_driver)
    
    token = login_page.get_access_token()
    
    assert token is None