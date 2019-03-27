import random

import requests
from bs4 import BeautifulSoup

PROXIES = [
    'http://188.225.9.121:8080',
]
ip = random.choice(PROXIES)
url = 'http://icanhazip.com/'
proxies = {'http': ip}
try:
    response = requests.get(url, proxies=proxies)  # 使用代理
    print(response.status_code)
    if response.status_code == 200:
        print(response.text)
except requests.ConnectionError as e:
    print(e.args)

# requests.get('https://google.com/serach?q=site%3Awww.neusoft.com+intitle%3A"大数据"%7Cintitle%3A"人工智能"%7Cintitle%3A"云计算"', proxies=proxies)
text=requests.get('http://google.com', proxies=proxies)
print(text.text)

