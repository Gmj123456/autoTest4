import pytest
import requests
import logging
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from config.config import USERNAME,PASSWORD,PTUSER_USERNAME, PTUSER_PASSWORD,GETMENU

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # 配置日志

from config.config import CHROME_DRIVER_PATH
logging.info(f"使用的 ChromeDriver 路径: {CHROME_DRIVER_PATH}")

"""特殊权限账号专用浏览器实例（保持打开直到菜单获取结束）"""
@pytest.fixture(scope="session")
def ptuser_driver():
    """特殊权限账号专用浏览器实例（保持打开直到测试结束）"""
    service = Service(str(CHROME_DRIVER_PATH))
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    # 浏览器关闭逻辑将延迟到所有测试结束后执行
    driver.quit()

"""一次性特殊权限账号登录"""
@pytest.fixture(scope="session")
def ptuser_logged_in(ptuser_driver):
    """一次性特殊权限账号登录"""
    login_page = LoginPage(ptuser_driver)
    result = login_page.login(PTUSER_USERNAME, PTUSER_PASSWORD)
    if not result:
        pytest.fail("特殊账号登录失败")

    # 获取token后不关闭浏览器
    token = login_page.get_access_token()

    # 返回token时保持浏览器打开
    yield token

    # 实际关闭浏览器的操作由ptuser_driver的teardown完成

"""提取菜单URL（整个测试会话只获取一次）"""
@pytest.fixture(scope="session")
def menu_urls(ptuser_logged_in, ptuser_driver):
    """提取菜单URL（整个测试会话只获取一次）"""
    response = None
    try:
        # 添加完整的请求头
        headers = {
            'Tenant-Id': '1',
            'accept': 'application/json, text/plain, */*',
            'X-Access-Token': ptuser_logged_in
        }

        response = requests.get(
            url=GETMENU,
            headers=headers,
            timeout=10
        )

        # 添加响应内容验证
        logging.debug(f"响应状态码: {response.status_code}")
        logging.debug(f"响应内容类型: {response.headers.get('Content-Type')}")
        logging.debug(f"响应前1000字符: {response.text[:1000]}")

        response.raise_for_status()

        # 验证内容类型是否为JSON
        if 'application/json' not in response.headers.get('Content-Type', ''):
            pytest.fail(f"接口返回非JSON数据，实际内容类型：{response.headers.get('Content-Type')}")

        # 增强JSON解析健壮性
        try:
            response_data = response.json()
        except json.JSONDecodeError as e:
            logging.error(f"JSON解析失败，响应内容：{response.text[:200]}")
            pytest.fail(f"接口返回非标准JSON数据：{str(e)}")

        # 验证数据结构
        if 'result' not in response_data:
            pytest.fail("接口响应缺少result字段")

        result_data = response_data['result']

        # 增强类型检查
        if not isinstance(result_data, list):
            logging.error(f"接口返回的result字段类型错误，实际类型：{type(result_data)}")
            pytest.fail(f"result字段应为list类型，实际得到：{type(result_data)}")

        # 添加详细日志
        logging.info(f"开始解析{len(result_data)}个根菜单项")
        menu_data = {}

        def extract_menu(menu):
            # 添加参数校验
            if not isinstance(menu, dict):
                logging.warning(f"非法菜单格式，期望dict实际得到: {type(menu)}")
                return {}

            menu_data = {}
            try:
                # 扩展支持的路径字段
                menu_path = menu.get('path') or menu.get('url') or ''
                menu_path = menu_path.strip('/')
                
                # 放宽组件校验条件
                if menu_path and not menu.get('hidden'):
                    # 使用更可靠的名称字段
                    menu_name = menu.get('title') or menu.get('name') or 'unknown'
                    # 生成标准化路径（修复多余斜杠问题）
                    full_path = f'/{menu_path}' 
                    
                    menu_data[menu_name] = full_path
                    logging.info(f"注册菜单项: {menu_name} -> {full_path}")

                # 增强子菜单路径拼接逻辑
                children = menu.get('children')
                if children is None:
                    children = []  # 如果 children 为 None，将其设为一个空列表
                for index, child in enumerate(children):
                    if isinstance(child, dict):
                        child_data = extract_menu(child)
                        # 修正路径拼接逻辑（处理嵌套路径）
                        if child_data and menu_path:
                            updated_data = {}
                            for name, path in child_data.items():
                                # 修正路径拼接逻辑（兼容ERP系统路由规范）
                                if path.startswith('/'):
                                    new_path = path  # 保留绝对路径
                                else:
                                    new_path = f'/{menu_path}/{path}'
                                updated_data[name] = new_path
                            child_data = updated_data
                        menu_data.update(child_data)
                    else:
                        logging.warning(f"跳过非法子菜单类型: {type(child)}")
                        
            except Exception as e:
                logging.error(f"解析菜单异常: {str(e)}", exc_info=True)
                
            return menu_data

        for root_menu in result_data:
            if not isinstance(root_menu, dict):
                logging.warning(f"跳过非字典类型的根菜单: {root_menu}")
                continue
            menu_data.update(extract_menu(root_menu))

        logging.info(f"提取到的菜单项: {menu_data}")
        logging.info(f"共提取到{len(menu_data)}个菜单项")
        return menu_data

    except Exception as e:
        # 初始化 error_msg 必须在前
        error_msg = f"菜单获取失败: {str(e)}"
        
        # 合并 response 存在性检查
        if response is not None:
            error_msg += f"\nHTTP状态码：{response.status_code}"
            error_msg += f"\n完整响应内容（前1000字符）: {response.text[:1000]}"
        else:
            error_msg += "\n（请求未完成或未获得响应）"
        
        pytest.fail(error_msg)



@pytest.fixture(scope="function")
def logged_in_driver():
    """测试账号浏览器实例"""
    service = Service(str(CHROME_DRIVER_PATH))
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in():
    """测试账号登录"""
    login_page = LoginPage(logged_in_driver)
    result = login_page.login(USERNAME,PASSWORD)
    if not result:
        pytest.fail("登录失败")

    yield
