# utils/ocr.py
import requests

def recognize_captcha(image_path):
    # 这里需要替换为实际的 OCR 接口 URL 和请求参数
    url = "https://your-ocr-api-url.com"
    files = {'image': open(image_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json().get('text')
    return ""