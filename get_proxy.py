import random

import requests

import lxml
import crawler_constant
from bs4 import BeautifulSoup

random_ua = random.choice(crawler_constant.USER_AGENTS)
headers = {
    'User-Agent': random_ua,
    'Connection': 'close'}
response = requests.get("http://www.data5u.com/free/gwgn/index.shtml", headers=headers).content
soup = BeautifulSoup(response, "lxml")
wlist = soup.find_all(class_='wlist')
wlist.find
print(result)
