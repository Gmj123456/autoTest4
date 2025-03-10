import base64
import requests
import time

API_KEY = 'ImVoymtJPMYkIx8icn0VRBRy'
SECRET_KEY = '2GFyE5r22o2vh6b1FrTxFF4hslUz6SKO'

# 硬编码的 access_token
HARDCODED_ACCESS_TOKEN = '24.c9fd59e5d5a36aac446d36a5a80d2e9e.2592000.1742362951.282335-117554037'
# 假设硬编码的 access_token 还剩的有效时长（秒），你可以根据实际情况调整
HARDCODED_EXPIRE_TIME = 2592000
# 缓存 access_token 及其过期时间
CACHED_ACCESS_TOKEN = HARDCODED_ACCESS_TOKEN
CACHE_EXPIRATION_TIME = time.time() + HARDCODED_EXPIRE_TIME

def get_access_token():
    """
    获取百度 AI 平台的 access_token
    """
    global CACHED_ACCESS_TOKEN, CACHE_EXPIRATION_TIME
    current_time = time.time()
    # 检查缓存的 access_token 是否有效
    if CACHED_ACCESS_TOKEN and current_time < CACHE_EXPIRATION_TIME:
        return CACHED_ACCESS_TOKEN

    # 鉴权接口的 URL
    auth_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    try:
        # 发送 GET 请求获取 access_token
        response = requests.get(auth_url, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()
        CACHED_ACCESS_TOKEN = result.get('access_token')
        # 设置缓存过期时间，有效期一般为 2592000 秒（30 天）
        CACHE_EXPIRATION_TIME = current_time + result.get('expires_in', 2592000)
        return CACHED_ACCESS_TOKEN
    except requests.RequestException as e:
        print(f"请求 access_token 时出现网络异常: {e}")
    except ValueError as e:
        print(f"解析 access_token 响应的 JSON 数据时出错: {e}")
    return None

def ocr_accurate_basic():
    """
    通用文字识别（高精度版）
    """
    # 通用文字识别（高精度版）的请求 URL
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    try:
        with open('../captcha.png', 'rb') as f:
            img = base64.b64encode(f.read())
    except FileNotFoundError:
        print("未找到图片文件 'captcha.png'")
        return

    # 获取 access_token
    access_token = get_access_token()
    if access_token is None:
        return

    # 拼接请求 URL
    request_url = request_url + "?access_token=" + access_token
    # 设置请求头
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 设置请求参数
    params = {"image": img}
    try:
        # 发送 POST 请求
        response = requests.post(request_url, data=params, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        res = response.json()
        if 'error_code' in res:
            # 如果返回错误码为 110（access_token 无效），则重新获取 access_token 并再次请求
            if res['error_code'] == 110:
                print("access_token 无效，重新获取...")
                new_access_token = get_access_token()
                if new_access_token:
                    new_request_url = request_url.replace(access_token, new_access_token)
                    new_response = requests.post(new_request_url, data=params, headers=headers, timeout=10)
                    new_response.raise_for_status()
                    new_res = new_response.json()
                    if 'error_code' in new_res:
                        print(f"文字识别请求出错，错误码: {new_res['error_code']}，错误信息: {new_res['error_msg']}")
                    else:
                        try:
                            res2 = new_res['words_result'][0]['words']
                            print(res2)
                        except (KeyError, IndexError):
                            print("解析文字识别响应结果时出错，请检查响应数据格式。")
                            print("完整的响应数据:", new_res)
            else:
                print(f"文字识别请求出错，错误码: {res['error_code']}，错误信息: {res['error_msg']}")
        else:
            try:
                res2 = res['words_result'][0]['words']
                print(res2)
            except (KeyError, IndexError):
                print("解析文字识别响应结果时出错，请检查响应数据格式。")
                print("完整的响应数据:", res)
    except requests.RequestException as e:
        print(f"文字识别请求时出现网络异常: {e}")
    except ValueError as e:
        print(f"解析文字识别响应的 JSON 数据时出错: {e}")


if __name__ == "__main__":
    ocr_accurate_basic()