import os

# 定义文件结构
file_structure = {
    "erp_web_test": {
        "config": ["config.py"],
        "pages": ["base_page.py", "login_page.py", "sales_plan_page.py"],
        "testcase": ["conftest.py", "test_sales_plan.py"],
        "utils": ["ocr.py"],
        "": ["requirements.txt", "run_tests.py"]
    }
}


def create_structure(structure, base_path=""):
    for key, value in structure.items():
        path = os.path.join(base_path, key)
        if isinstance(value, list):
            # 创建文件夹
            if not os.path.exists(path):
                os.makedirs(path)
            # 创建文件
            for file in value:
                file_path = os.path.join(path, file)
                with open(file_path, 'w') as f:
                    pass
        elif isinstance(value, dict):
            # 递归创建子文件夹和文件
            if not os.path.exists(path):
                os.makedirs(path)
            create_structure(value, path)


if __name__ == "__main__":
    create_structure(file_structure)
