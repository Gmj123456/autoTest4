# 测试之前先登录管理员账户获取菜单url
import requests

# 菜单接口 URL
url = 'http://192.168.150.111:8099/erp/sys/permission/list'

# 设置请求头，带上 token
headers = {
  'Tenant-Id': '1',
  'accept': 'application/json, text/plain, */*',
  'X-Access-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE4NzE0NDExMjc1Mzg4MTQ5NzgiLCJleHAiOjE3NDE5NTIyMTksInVzZXJuYW1lIjoicHR1c2VyIiwicmVhbG5hbWUiOiLns7vnu5_nrqHnkIblkZgifQ.1pf6OcKyzj8jfrXer-PQdwALpFl0zyhTUn5lmVjZFc4'
}

try:
  # 发送 GET 请求
  response = requests.get(url, headers=headers)

  # 尝试解析 JSON 响应
  response_data = response.json()

  # 打印整个响应内容用于调试
  # print(response_data)

  # 检查 HTTP 状态码是否为 2xx 成功响应
  if response.status_code // 100 == 2:
    # 根据 API 文档确定如何判断请求是否成功
    # 假设响应数据中包含 'success' 字段
    if 'success' in response_data and response_data['success']:
      result = response_data.get('result', 'No result field found')
      print('请求成功，返回的数据如下：', result)
    else:
      print('请求失败，原因：', response_data.get('message', '未知错误'))
  else:
    print(f'请求失败，状态码: {response.status_code}')
    print(response.text)

except requests.RequestException as e:
  print(f'请求发生错误: {str(e)}')
