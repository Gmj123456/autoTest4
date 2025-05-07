# autoTest 自动化测试项目

## 项目概述
`autoTest` 是一个基于 Python、Selenium 和 `pytest` 框架构建的自动化测试项目，主要用于对特定 Web 应用（如 ERP 系统）进行自动化测试。该项目包含登录、销售计划添加等功能的自动化测试脚本，同时具备日志管理、验证码识别等辅助功能，可有效提高测试效率和准确性。

## 项目结构autoTest1
├── README.md
├── auto_git_push.sh
├── requirements.txt
├── .idea/
├── utils/
├── testdata/
├── config/
├── logs/
├── testcase/
├── pages/
└── __pycache__/
### 主要目录和文件说明
- **`.idea/`**：JetBrains IDE（如 PyCharm）的项目配置文件。
- **`utils/`**：存放工具函数和脚本，如日志管理、验证码识别等。
    - `logger.py`：统一配置日志，将日志信息同时输出到文件和控制台。
    - `ocr.py`：调用百度 AI 平台的通用文字识别接口识别验证码图片。
- **`testdata/`**：存储测试数据，如 `sales_plan_data.json` 包含销售计划添加测试的月份和计划数量数据。
- **`config/`**：包含项目的配置文件，如 `config.py` 存储了百度 AI 平台的 `API_KEY` 和 `SECRET_KEY`，以及登录所需的账号密码等信息。

# 调Kimi接口配置
KIMI_BASE_URL ="https://api.moonshot.cn/v1"
- **`logs/`**：存储项目的日志文件，日志文件名包含时间戳，如 `automation_20240101120000.log` 记录项目运行过程中的日志信息。日志配置在 `utils/logger.py` 中，示例如下：# utils/logger.py
def setup_logging():
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    # ... 其他日志配置 ...- **`testcase/`**：存放测试用例脚本，使用 `pytest` 框架编写。
    - `conftest.py`：定义了多个测试固件，如浏览器实例、登录状态等。
    - `test_sales_plan.py`：包含销售计划菜单跳转和销售计划添加功能的测试用例。
    - `test_addsalesplan.py`：销售计划添加的测试用例。
- **`pages/`**：存放页面对象类，封装了页面元素和操作方法。
    - `base_page.py`：定义了基础页面对象类，包含通用的操作方法。
    - `login_page.py`：封装了登录页面的操作，如保存验证码图片、识别验证码、登录、退出登录等功能。
    - `sales_plan_page.py`：封装了销售计划页面的操作，如导航到销售计划页面、添加销售计划等功能。

## 技术栈
- **编程语言**：Python
- **测试框架**：`pytest`
- **自动化测试工具**：Selenium
- **日志管理**：Python `logging` 模块
- **验证码识别**：百度 AI 平台的通用文字识别（高精度版）接口

## 环境准备
1. **安装 Python**：确保已安装 Python 3.x 版本。
2. **安装依赖库**：在项目根目录下执行以下命令安装所需的依赖库：pip install -r requirements.txt3. **配置百度 AI 平台**：在 `config/config.py` 中配置百度 AI 平台的 `API_KEY` 和 `SECRET_KEY`。
4. **配置 ChromeDriver**：下载与 Chrome 浏览器版本匹配的 ChromeDriver，并将其路径配置到 `config/config.py` 中的 `CHROME_DRIVER_PATH`。
5. **配置测试账号和 URL**：在 `config/config.py` 中配置测试账号和相关 URL。
6. **配置 Kimi 接口**：在 `config/config.py` 中配置调用 Kimi 接口所需的信息。

## 运行测试
在项目根目录下执行以下命令运行测试：pytest testcase/
## 日志查看
测试过程中的日志信息会记录在 `logs/` 目录下，文件名包含时间戳，例如 `automation_20240101120000.log`，可通过查看该文件了解测试运行情况。

## 自动提交脚本
项目提供了一个自动提交并推送代码的 Bash 脚本 `auto_git_push.sh`，可在项目根目录下执行以下命令自动提交并推送代码：./auto_git_push.sh "提交信息"若不提供提交信息，默认提交信息为 "Auto commit"。

## 注意事项
- 请确保网络连接正常，以便调用百度 AI 平台的验证码识别接口和获取菜单数据的 API。
- 若测试过程中出现验证码识别失败的情况，可能需要调整 `utils/ocr.py` 脚本或手动处理验证码。示例代码如下：# utils/ocr.py
def read_image(self, image_path):
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read())
    except FileNotFoundError:
        logging.error("未找到图片文件 '%s'", image_path)
        return None- 若使用不同的浏览器，需要相应地配置浏览器驱动，并更新 `config/config.py` 中的 `CHROME_DRIVER_PATH`。
- 运行测试前，请确保 `testdata/sales_plan_data.json` 文件存在，用于参数化测试用例。

## 贡献
欢迎对本项目进行贡献，可通过提交 Pull Request 或 Issues 来提出改进建议。

## 许可证
本项目遵循 [MIT 许可证](https://opensource.org/licenses/MIT)。    