import requests

# 定义接口 URL
url = 'http://192.168.150.222:3067/erp/system/permission'

# 定义 token，这里需要替换为实际的 token 值
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE4NTMyMzM5MjA5MDUwODA4MzMiLCJleHAiOjE3NDE3OTQxNzksInVzZXJuYW1lIjoiZ3VvbWoiLCJyZWFsbmFtZSI6IumDreaipuWohyjmraPlvI8pIn0.QBMhODEHoT38FZlhC50B5OVURbtsMBPSmvsKfrh3yh4'

# 设置请求头，带上 token
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',  # 示例
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # 模拟浏览器的 User-Agent
    'X-Requested-With': 'XMLHttpRequest',  # 部分框架需要
}

try:
    # 发送  请求
    response = requests.post(url, headers=headers)



    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应的 JSON 数据
        data = response.json()
        print('请求成功，返回的数据如下：')
        print(data)
    else:
        print(f'请求失败，状态码: {response.status_code}')
        print(response.text)
except requests.RequestException as e:
    print(f'请求发生错误: {e}')