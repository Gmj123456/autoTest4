import pytest
import requests
import logging  # 重新导入 logging 模块
from utils.logger import setup_logging
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, PTUSER_USERNAME, PTUSER_PASSWORD, GETMENU
import datetime

# 调用统一的日志配置
logger = setup_logging()

from config.config import CHROME_DRIVER_PATH
# 记录使用的 ChromeDriver 路径
logging.info(f"使用的 ChromeDriver 路径: {CHROME_DRIVER_PATH}")

"""
特殊权限账号专用浏览器实例并登录获取 token（保持打开直到菜单获取结束）

此 fixture 用于创建一个 Chrome 浏览器实例，使用特殊权限账号登录，并获取访问 token。
浏览器会保持打开状态，直到菜单获取结束。

:return: 包含 token 和浏览器驱动实例的元组
"""
@pytest.fixture(scope="session")
def ptuser_driver_and_logged_in():
    # 创建 Chrome 浏览器服务实例
    service = Service(str(CHROME_DRIVER_PATH))
    # 创建 Chrome 浏览器驱动实例
    driver = webdriver.Chrome(service=service)
    # 最大化浏览器窗口
    driver.maximize_window()
    # 创建登录页面实例
    login_page = LoginPage(driver)
    # 使用特殊权限账号进行登录
    result = login_page.login(PTUSER_USERNAME, PTUSER_PASSWORD)
    # 检查登录是否成功，若失败则终止测试
    if not result:
        pytest.fail("特殊账号登录失败")

    # 获取访问 token，获取后不关闭浏览器
    token = login_page.get_access_token_ptuser()

    # 返回 token 和浏览器驱动实例，保持浏览器打开
    yield token, driver

    # 退出特殊权限账号
    login_page.logout()
    # 关闭浏览器
    driver.quit()

"""
提取菜单 URL（整个测试会话只获取一次）

此 fixture 用于从 API 获取菜单数据，并提取其中的菜单 URL。
整个测试会话期间只会执行一次。

:param ptuser_driver_and_logged_in: 包含特殊权限账号 token 和浏览器驱动实例的元组
:return: 包含菜单名称和对应 URL 的字典
"""
@pytest.fixture(scope="session")
def menu_urls(ptuser_driver_and_logged_in):
    # 从元组中解包特殊权限账号的 token 和浏览器驱动实例
    ptuser_logged_in, ptuser_driver = ptuser_driver_and_logged_in
    # 初始化响应对象
    response = None
    try:
        # 添加完整的请求头
        headers = {
            'Tenant-Id': '1',
            'accept': 'application/json, text/plain, */*',
            'X-Access-Token': ptuser_logged_in
        }

        # 发送 GET 请求获取菜单数据
        response = requests.get(
            url=GETMENU,
            headers=headers,
            timeout=10
        )

        # 记录响应状态码
        logging.debug(f"响应状态码: {response.status_code}")
        # 记录响应内容类型
        logging.debug(f"响应内容类型: {response.headers.get('Content-Type')}")
        # 记录响应前 1000 字符
        # logging.debug(f"响应前 1000 字符: {response.text[:1000]}")

        # 检查响应状态码，若不是 200 则抛出异常
        response.raise_for_status()

        # 验证内容类型是否为 JSON
        if 'application/json' not in response.headers.get('Content-Type', ''):
            pytest.fail(f"接口返回非 JSON 数据，实际内容类型：{response.headers.get('Content-Type')}")

        # 增强 JSON 解析健壮性
        try:
            # 解析响应内容为 JSON 格式
            response_data = response.json()
        except json.JSONDecodeError as e:
            # 记录 JSON 解析失败信息
            logging.error(f"JSON 解析失败，响应内容：{response.text[:200]}")
            # 若解析失败则终止测试
            pytest.fail(f"接口返回非标准 JSON 数据：{str(e)}")

        # 验证数据结构，检查是否包含 'result' 字段
        if 'result' not in response_data:
            pytest.fail("接口响应缺少 result 字段")

        # 获取响应数据中的 'result' 字段
        result_data = response_data['result']

        # 增强类型检查，确保 'result' 字段为列表类型
        if not isinstance(result_data, list):
            # 记录 'result' 字段类型错误信息
            logging.error(f"接口返回的 result 字段类型错误，实际类型：{type(result_data)}")
            # 若类型错误则终止测试
            pytest.fail(f"result 字段应为 list 类型，实际得到：{type(result_data)}")

        # 记录开始解析根菜单项的信息
        logging.info(f"开始解析{len(result_data)}个根菜单项")
        # 初始化菜单数据字典
        menu_data = {}

        def extract_menu(menu):
            """
            递归提取菜单信息

            :param menu: 菜单数据字典
            :return: 包含菜单名称和对应 URL 的字典
            """
            # 检查菜单数据是否为字典类型
            if not isinstance(menu, dict):
                # 若不是字典类型则记录警告信息
                logging.warning(f"非法菜单格式，期望 dict 实际得到: {type(menu)}")
                return {}

            # 初始化当前菜单数据字典
            menu_data = {}
            try:
                # 扩展支持的路径字段，优先使用 'path'，其次是 'url'
                menu_path = menu.get('path') or menu.get('url') or ''
                # 去除路径前后的斜杠
                menu_path = menu_path.strip('/')

                # 放宽组件校验条件，若路径存在且菜单未隐藏
                if menu_path and not menu.get('hidden'):
                    # 使用更可靠的名称字段，优先使用 'title'，其次是 'name'
                    menu_name = menu.get('title') or menu.get('name') or 'unknown'
                    # 生成标准化路径，添加前导斜杠
                    full_path = f'/{menu_path}'

                    # 将菜单名称和路径添加到菜单数据字典中
                    menu_data[menu_name] = full_path
                    # 记录注册菜单项的信息
                    # logging.info(f"注册菜单项: {menu_name} -> {full_path}")

                # 获取菜单的子菜单列表
                children = menu.get('children')
                # 若子菜单列表为 None，则将其设为一个空列表
                if children is None:
                    children = []
                # 遍历子菜单列表
                for index, child in enumerate(children):
                    # 检查子菜单是否为字典类型
                    if isinstance(child, dict):
                        # 递归提取子菜单信息
                        child_data = extract_menu(child)
                        # 若子菜单信息存在且当前菜单路径存在
                        if child_data and menu_path:
                            # 初始化更新后的子菜单数据字典
                            updated_data = {}
                            # 遍历子菜单信息
                            for name, path in child_data.items():
                                # 修正路径拼接逻辑，兼容 ERP 系统路由规范
                                if path.startswith('/'):
                                    new_path = path  # 保留绝对路径
                                else:
                                    new_path = f'/{menu_path}/{path}'
                                # 将更新后的路径添加到更新后的子菜单数据字典中
                                updated_data[name] = new_path
                            # 更新子菜单信息
                            child_data = updated_data
                        # 将子菜单信息合并到当前菜单数据字典中
                        menu_data.update(child_data)
                    else:
                        # 若子菜单不是字典类型则记录警告信息
                        logging.warning(f"跳过非法子菜单类型: {type(child)}")

            except Exception as e:
                # 记录解析菜单异常信息
                logging.error(f"解析菜单异常: {str(e)}", exc_info=True)

            return menu_data

        # 遍历根菜单项列表
        for root_menu in result_data:
            # 检查根菜单项是否为字典类型
            if not isinstance(root_menu, dict):
                # 若不是字典类型则记录警告信息
                logging.warning(f"跳过非字典类型的根菜单: {root_menu}")
                continue
            # 合并根菜单项信息到菜单数据字典中
            menu_data.update(extract_menu(root_menu))

        # 记录提取到的菜单项信息
        # logging.info(f"提取到的菜单项: {menu_data}")
        # 记录共提取到的菜单项数量
        logging.info(f"共提取到{len(menu_data)}个菜单项")
        
        # 新增保存到JSON文件的代码
        menu_file = r"d:\gmj\workSpaces\workSpaces_pycharm\autoTest1\menu.json"
        try:
            with open(menu_file, 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, ensure_ascii=False, indent=4)
            logging.info(f"菜单数据已保存至: {menu_file}")
        except Exception as e:
            logging.error(f"菜单数据保存失败: {str(e)}")

        return menu_data

    except Exception as e:
        # 初始化错误信息
        error_msg = f"菜单获取失败: {str(e)}"

        # 若响应对象存在
        if response is not None:
            # 添加 HTTP 状态码到错误信息中
            error_msg += f"\nHTTP 状态码：{response.status_code}"
            # 添加完整响应内容（前 1000 字符）到错误信息中
            error_msg += f"\n完整响应内容（前 1000 字符）: {response.text[:1000]}"
        else:
            # 若响应对象不存在，添加请求未完成或未获得响应信息到错误信息中
            error_msg += "\n（请求未完成或未获得响应）"

        # 若出现异常则终止测试
        pytest.fail(error_msg)

    finally:
        # 手动调用退出和关闭操作
        login_page = LoginPage(ptuser_driver)
        login_page.logout()
        ptuser_driver.quit()

"""
测试账号登录，返回登录后的驱动实例

此 fixture 用于创建一个 Chrome 浏览器实例，使用测试账号登录，并返回登录后的驱动实例。
每个测试函数执行前都会重新创建浏览器实例并登录。

:return: 登录后的浏览器驱动实例
"""
@pytest.fixture(scope="function")
def logged_in():  # 依赖特殊权限账号的 fixture 已移除
    # 创建 Chrome 浏览器服务实例
    service = Service(str(CHROME_DRIVER_PATH))
    # 创建 Chrome 浏览器驱动实例
    driver = webdriver.Chrome(service=service)
    # 最大化浏览器窗口
    driver.maximize_window()
    # 创建登录页面实例
    login_page = LoginPage(driver)
    # 使用测试账号进行登录
    result = login_page.login(USERNAME, PASSWORD)
    # 检查登录是否成功，若失败则终止测试
    if not result:
        pytest.fail("登录失败")
    # 返回登录后的浏览器驱动实例
    yield driver

    # 关闭浏览器
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """记录测试用例开始时间"""
    start_time = datetime.datetime.now()
    logger.info(f"Test case {item.name} started at {start_time}")
    outcome = yield
    # 这里可以添加更多的清理逻辑

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """记录测试用例结束时间"""
    outcome = yield
    end_time = datetime.datetime.now()
    logger.info(f"Test case {item.name} ended at {end_time}")
    # 这里可以添加更多的清理逻辑