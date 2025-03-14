import json
import time
import pytest
import logging
from selenium import webdriver
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, PTUSER_USERNAME, PTUSER_PASSWORD
from selenium.webdriver.chrome.service import Service
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前脚本的绝对路径
script_dir = Path(__file__).resolve().parent
# 构建 chromedriver 的相对路径
CHROME_DRIVER_PATH = script_dir.parent / 'utils' / 'chromedriver.exe'
logging.info(f"使用的 ChromeDriver 路径: {CHROME_DRIVER_PATH}")


@pytest.fixture(scope="session")
def driver():
    # 使用 Service 类指定 ChromeDriver 的位置
    service = Service(str(CHROME_DRIVER_PATH))
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()  # 设置全屏
    time.sleep(1)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    result = login_page.login(USERNAME, PASSWORD)

    if result:
        logging.info("登录成功")
        yield driver
    else:
        pytest.fail("登录失败")


@pytest.fixture(scope="function")
def pt_logged_in_driver(driver):
    """特殊权限账号登录"""
    login_page = LoginPage(driver)
    result = login_page.login(PTUSER_USERNAME, PTUSER_PASSWORD)
    if not result:
        pytest.fail("特殊账号登录失败")
    yield driver


@pytest.fixture(scope="function")
def admin_access_token(pt_logged_in_driver):
    """获取特殊账号的token"""
    login_page = LoginPage(pt_logged_in_driver)
    return login_page.get_access_token()


@pytest.fixture(scope="session")
def ptuser_driver():
    """特殊权限账号专用浏览器实例（保持打开直到测试结束）"""
    service = Service(str(CHROME_DRIVER_PATH))
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    # 浏览器关闭逻辑将延迟到所有测试结束后执行
    driver.quit()


@pytest.fixture(scope="session")
def ptuser_logged_in(ptuser_driver):
    """一次性特殊权限账号登录"""
    login_page = LoginPage(ptuser_driver)
    result = login_page.login(PTUSER_USERNAME, PTUSER_PASSWORD)  # 现在可以正确引用配置
    if not result:
        pytest.fail("特殊账号登录失败")

    # 获取token后不关闭浏览器
    token = login_page.get_access_token()

    # 返回token时保持浏览器打开
    yield token

    # 实际关闭浏览器的操作由ptuser_driver的teardown完成


def extract_menu(menu_node, base_path=""):
    menu_data = {}
    # 加强字段存在性校验
    if not all(key in menu_node for key in ['title', 'component']):
        logging.error(f"菜单节点缺少必要字段: {menu_node}")
        return menu_data

    # 路径生成增强容错
    current_path = menu_node.get('path', '').strip('/') or menu_node.get('url', '').strip('/')
    full_path = '/'.join(filter(None, [base_path, current_path])) if base_path or current_path else ''
    full_path = full_path.lstrip('/')

    # 记录完整路径生成过程
    logging.debug(f"处理菜单: {menu_node['title']} | 当前路径: {current_path} | 最终路径: /{full_path}")

    # 收集有效菜单项（必须包含组件且非隐藏）
    if menu_node.get('component') and not menu_node.get('hidden'):
        menu_data[menu_node['title']] = f'/{full_path}'
        logging.debug(f"有效菜单: {menu_node['title']} -> /{full_path}")

    # 递归处理子菜单（增强容错）
    for child in menu_node.get('children', []):
        if isinstance(child, dict):
            # 子菜单继承当前路径
            child_menu_data = extract_menu(child, full_path)
            menu_data.update(child_menu_data)
        else:
            logging.warning(f"非法子菜单类型: {type(child)}")

    return menu_data


@pytest.fixture(scope="session")
def menu_urls(ptuser_logged_in, ptuser_driver):
    """提取菜单URL（整个测试会话只获取一次）"""
    import requests
    response = None
    try:
        # 添加完整的请求头
        headers = {
            'Tenant-Id': '1',
            'accept': 'application/json, text/plain, */*',
            'X-Access-Token': ptuser_logged_in
        }

        response = requests.get(
            "http://192.168.150.111:8099/erp/sys/permission/list",
            headers=headers,
            timeout=10
        )

        # 添加响应内容验证
        logging.debug(f"响应状态码: {response.status_code}")
        logging.debug(f"响应内容类型: {response.headers.get('Content-Type')}")
        logging.debug(f"响应前200字符: {response.text[:200]}")

        response.raise_for_status()

        # 验证内容类型是否为JSON
        if 'application/json' not in response.headers.get('Content-Type', ''):
            pytest.fail(f"接口返回非JSON数据，实际内容类型：{response.headers.get('Content-Type')}")

        # 将接口返回数据保存到文件
        with open('outurl.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)

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
        
        # 添加额外信息
        if response is not None:
            error_msg += f"\nHTTP状态码：{response.status_code}"
            error_msg += f"\n完整响应内容（前1000字符）: {response.text[:1000]}"
        else:
            error_msg += "\n（请求未完成或未获得响应）"
        
        pytest.fail(error_msg)


def test_menu_structure(menu_urls):
    assert menu_urls, "未获取到任何菜单项"
    for menu_title, url in menu_urls.items():
        assert url.startswith('/'), f"URL {url} 格式错误"
