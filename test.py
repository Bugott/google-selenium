import random

import requests
from bs4 import BeautifulSoup

PROXIES = [
    'http://139.99.57.60:8080',
]
ip = random.choice(PROXIES)
print(ip)
url = 'http://icanhazip.com/'
proxies = {'http': ip}
# try:
#     response = requests.get(url, proxies=proxies)  # 使用代理
#     response.close()
#     print(response.status_code)
#     if response.status_code == 200:
#         print(response.text)
# except requests.ConnectionError as e:
#     print(e.args)
#
# # requests.get('https://google.com/serach?q=site%3Awww.neusoft.com+intitle%3A"大数据"%7Cintitle%3A"人工智能"%7Cintitle%3A"云计算"', proxies=proxies)
# requests.get('http://google.com', proxies=proxies)

html = '''
<span class="st"><span class="f">2017年7月11日</s> <b>...</b> 随着国家环保部信息中心生态环境监测<b>大数据</b>应用(一期)建设项目通过终验，环境<br/>
质量监测数据全国联网、互联互通、通存通取技术基础宣告建立。</span>
'''
soup = BeautifulSoup(html, 'lxml')
for s in soup.strings:
    print(s)