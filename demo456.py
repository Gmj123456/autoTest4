import requests

# 定义接口 URL
url = 'http://192.168.150.111:8099/erp/sys/permission/list?_t=1741770298'
# url = 'http://192.168.150.111:8099/erp/sys/permission/getUserPermissionByToken'
# url = 'http://192.168.150.111:8099/erp/aiCheckTexts/list?_t=1741770150&column=createTime&order=desc&pageNo=1&pageSize=30'

# 定义 token，这里需要替换为实际的 token 值
# token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE4NTMyMzM5MjA5MDUwODA4MzMiLCJleHAiOjE3NDE3OTQxNzksInVzZXJuYW1lIjoiZ3VvbWoiLCJyZWFsbmFtZSI6IumDreaipuWohyjmraPlvI8pIn0.QBMhODEHoT38FZlhC50B5OVURbtsMBPSmvsKfrh3yh4'

# 设置请求头，带上 token
res = {
    # 'X-Access-Token':  {token}
    'X-Access-Token':  'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE4NTMyMzM5MjA5MDUwODA4MzMiLCJleHAiOjE3NDE3OTk2MDAsInVzZXJuYW1lIjoiZ3VvbWoiLCJyZWFsbmFtZSI6IumDreaipuWohyjmraPlvI8pIn0.mm3P3lD3RghYEj9fQ0TFAPUQc68UHUx3SJwunU0qUMY'
}

try:
    # 发送  请求
    response = requests.get(url, headers=res)

    print(response.json())
    # 检查响应状态码
    # if response.status_code == 200:
    #     # 解析响应的 JSON 数据
    #     data = response.json()
    #     print('请求成功，返回的数据如下：')
    #     print(data)
    # else:
    #     print(f'请求失败，状态码: {response.status_code}')
    #     print(response.text)
except requests.RequestException as e:
    print(f'请求发生错误: {e}')