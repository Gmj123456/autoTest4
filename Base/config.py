# config/config.py
from pathlib import Path

project_root = Path(__file__).parent.parent
CHROME_DRIVER_PATH = project_root / 'Base' / 'utils' / 'chromedriver.exe'

# ERP_URL = "http://192.168.150.222:3066"  # 本地环境
# LOGIN_SUCCESS_URL = "http://192.168.150.222:3066/dashboard/analysis"

ERP_URL = "http://124.222.178.125:3006" # 测试环境
LOGIN_SUCCESS_URL = "http://124.222.178.125:3006/dashboard/analysis"

USERNAME = "guomj"  # 主测试账号
PASSWORD = "gmj123.."

PTUSER_USERNAME = "ptuser"  # 特殊权限账号
PTUSER_PASSWORD = "qwe123"
GETMENU = "http://192.168.150.111:8099/erp/sys/permission/list"  #  请求菜单url接口

# ocr识别
API_KEY = '5mPZWWtbEIcYzeFKmhpQ0Cat'
SECRET_KEY = 'GBd6NyH5oBqXzrZfkyAsKSChKlZEMMTk'
