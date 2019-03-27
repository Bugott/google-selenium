import requests
import random

# 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
order = "cc07a80256ba5db9fa1af10c6edd5a09"
# 获取IP的API接口
apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=cc07a80256ba5db9fa1af10c6edd5a09"
# 要抓取的目标网站地址
targetUrl = "https://www.google.com"
try:
    # 获取IP列表
    # print(apiUrl)
    # res = requests.get(apiUrl).text.strip("\n")
    # # 按照\n分割获取到的IP
    # ips = res.split("\n")
    # # 随机选择一个IP
    # proxyip = random.choice(ips)
    # 使用代理IP请求目标网址
    r = requests.get(targetUrl, proxies={'http': 'http://' + '219.79.153.94:556'})
    html = r.content
    html_doc = str(html, 'utf-8')  # html_doc=html.decode("utf-8","ignore")
    # print(html_doc)l
    print(html_doc)
except Exception as e:
    print(e)
