from element_location.save_html import save_body_content_to_file
from element_location.kimi_upload_files import analyze_html_for_testing

save_body_content_to_file("http://192.168.150.222:3066/amzShipment/salesPlan" ,file_path='sales_plan_body.html')  # 保存页面<body>内容到文件
analyze_html_for_testing(ele_loc_file='sales_plan_element_location.json')  # 调用AI进行元素定位的识别