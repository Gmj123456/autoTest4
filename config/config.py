# config/config.py
from pathlib import Path

project_root = Path(__file__).parent.parent
CHROME_DRIVER_PATH = project_root / 'utils' / 'chromedriver.exe'
# CHROME_DRIVER_PATH = r'D:\gmj\workSpaces\workSpaces_pycharm\autoTest1\utils\chromedriver.exe'  # chromedriver.exe路径

ERP_URL = "http://192.168.150.222:3066/"
LOGIN_SUCCESS_URL = "http://192.168.150.222:3066/dashboard/analysis"

USERNAME = "guomj"  # 主测试账号
PASSWORD = "gmj123.."

PTUSER_USERNAME = "ptuser"  # 特殊权限账号
PTUSER_PASSWORD = "qwe123"
GETMENU = "http://192.168.150.111:8099/erp/sys/permission/list"  #  请求菜单url接口

# ocr识别
API_KEY = 'ImVoymtJPMYkIx8icn0VRBRy'
SECRET_KEY = '2GFyE5r22o2vh6b1FrTxFF4hslUz6SKO'