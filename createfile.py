import os
import sys

# 定义PageObject文件
page_object_files = [
    "PageObject/page_login.py",
    "PageObject/page_salesPlan.py",
    "PageObject/page_sales_orderScheduling.py",
    "PageObject/page_productionDeliveryPlan.py",
    "PageObject/page_orderAllocation.py",
    "PageObject/page_issueProductionOrder.py",
    "PageObject/page_shippingPlan.py",
    "PageObject/page_productionProgress.py",
    "PageObject/page_localInventoryManagement.py",
    "PageObject/page_delivery.py"
]

# 定义TestCase文件
test_case_files = [
    "TestCase/conftest.py",
    "TestCase/test_login.py",
    "TestCase/test_salesPlan.py",
    "TestCase/test_sales_orderScheduling.py",
    "TestCase/test_productionDeliveryPlan.py",
    "TestCase/test_orderAllocation.py",
    "TestCase/test_issueProductionOrder.py",
    "TestCase/test_shippingPlan.py",
    "TestCase/test_productionProgress.py",
    "TestCase/test_localInventoryManagement.py",
    "TestCase/test_delivery.py"
]


def create_file_structure():
    # 检查PageObject和TestCase目录是否存在
    if not os.path.exists("PageObject"):
        print("错误: PageObject目录不存在!")
        sys.exit(1)

    if not os.path.exists("TestCase"):
        print("错误: TestCase目录不存在!")
        sys.exit(1)

    # 创建TestCase下的子目录
    for directory in test_case_directories:
        os.makedirs(directory, exist_ok=True)
        print(f"创建目录: {directory}")

    # 创建页面对象文件
    for file_path in page_object_files:
        if os.path.exists(file_path):
            print(f"文件已存在，跳过: {file_path}")
            continue

        with open(file_path, "w", encoding="utf-8") as f:
            pass  # 创建空文件
        print(f"创建文件: {file_path}")

    # 创建测试用例文件
    for file_path in test_case_files:
        if os.path.exists(file_path):
            print(f"文件已存在，跳过: {file_path}")
            continue

        with open(file_path, "w", encoding="utf-8") as f:
            pass  # 创建空文件
        print(f"创建文件: {file_path}")

    print("文件结构创建完成！")


if __name__ == "__main__":
    # 检查是否有参数
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        create_file_structure()
    else:
        print("警告：此脚本将创建新文件。如果文件已存在，将跳过创建。")
        print("如需继续，请使用 --force 参数运行此脚本。")
        print("例如: python create_test_framework.py --force")
        sys.exit(1)
